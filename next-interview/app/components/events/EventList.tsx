'use client'
import { useState, useEffect } from 'react';
import { ApiGet, ApiPost } from '@/app/utils/Api';
import { IEvent } from '@/app/types';
import { Button } from "@/components/ui/button";
import { Skeleton } from "@/components/ui/skeleton";
import EventCard from './EventCard';
import EventDialog from './EventDialog';
import EventComments from './EventComments';

const EventSkeleton = () => (
  <div className="w-full max-w-md mb-6">
    <Skeleton className="w-full h-56 rounded-xl" />
    <Skeleton className="w-3/4 h-6 mt-2" />
    <Skeleton className="w-full h-4 mt-2" />
    <div className="flex justify-between items-center mt-2">
      <Skeleton className="w-20 h-8" />
      <Skeleton className="w-20 h-8" />
    </div>
  </div>
);

const EventList = () => {
  const [events, setEvents] = useState<IEvent[]>([]);
  const [newEvent, setNewEvent] = useState<Partial<IEvent>>({});
  const [isDialogOpen, setIsDialogOpen] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [selectedEventForComments, setSelectedEventForComments] = useState<IEvent | null>(null);
  const [isCommentsOpen, setIsCommentsOpen] = useState(false);
  const [commentOffset, setCommentOffset] = useState(0);
  const [commentHasMore, setCommentHasMore] = useState(false);

  useEffect(() => {
    fetchEvents();
  }, []);

  const fetchEvents = async () => {
    setIsLoading(true);
    try {
      const data = await ApiGet('event');
      // Ensure each event has a comments array initialized
      const eventsWithComments = data.map((event: any) => {
        const processedEvent: IEvent = {
          uqid: event.uqid,
          name: event.name,
          description: event.description,
          img_link: event.img_link,
          number_of_likes: event.number_of_likes,
          comments: event.comments && Array.isArray(event.comments) ? event.comments : [],
          total_comments: 0
        };
        return processedEvent;
      });
      console.log('Fetched events with comments initialized:', eventsWithComments);
      setEvents(eventsWithComments);
      
      // Fetch initial comments and metadata for each event
      await Promise.all(eventsWithComments.map((event: IEvent) => fetchInitialCommentsForEvent(event.uqid)));
    } catch (error) {
      console.error('Error fetching events:', error);
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateOrUpdateEvent = async () => {
    try {
      await ApiPost('event', newEvent);
      setNewEvent({});
      setIsDialogOpen(false);
      fetchEvents();
    } catch (error) {
      console.error('Error creating/updating event:', error);
    }
  };
  
  const handleLikeEvent = async (uqid: string) => {
    try {
      await ApiPost('event/like', { uqid });
      fetchEvents();
    } catch (error) {
      console.error('Error liking event:', error);
    }
  };

  const handleEditEvent = (event: IEvent) => {
    setNewEvent(event);
    setIsDialogOpen(true);
  };

  const handleViewComments = (event: IEvent) => {
    setSelectedEventForComments(event);
    setIsCommentsOpen(true);
    setCommentOffset(0);
    // Fetch comments for this event
    fetchCommentsForEvent(event.uqid, 0);
  };
  
  const ApiGetComments = async (event_uqid: string, limit: number = 20, offset: number = 0) => {
    const queryParams = new URLSearchParams({ 
      uqid: event_uqid,
      limit: limit.toString(),
      offset: offset.toString()
    });
    const route = `event/comments?${queryParams.toString()}`;
    
    return ApiGet(route);
  };

  const ApiLikeComment = async (comment_id: string) => {
    const payload = { comment_uqid: comment_id };
    console.log('Sending like comment request with payload:', payload);
    return ApiPost('event/comment/like', payload);
  };

  const fetchInitialCommentsForEvent = async (event_uqid: string) => {
    const limit = 20;
    try {
      console.log('Fetching initial comments for event:', event_uqid);
      const response = await ApiGetComments(event_uqid, limit, 0);
      const comments = response.comments;
      const pagination = response.pagination;
      console.log('Received initial comments response:', response);
      
      // Parse comments
      const parsedComments = comments.map((comment: any) => ({
        id: comment.uqid,
        uqid: comment.event_uqid,
        user: comment.user,
        text: comment.text,
        created_at: comment.created_at || new Date().toISOString(),
        number_of_likes: comment.number_of_likes || 0
      }));
      
      // Update the main events array with initial comments and total count
      setEvents((prevEvents) =>
        prevEvents.map((event) =>
          event.uqid === event_uqid
            ? {
                ...event,
                comments: parsedComments,
                total_comments: pagination?.total || 0
              }
            : event
        )
      );
      
      console.log('Updated event with initial comments. Total:', pagination?.total);
    } catch (error) {
      console.error('Error fetching initial comments:', error);
    }
  };

  const fetchCommentsForEvent = async (event_uqid: string, offset: number = 0) => {
    const limit = 20;
    try {
      console.log('Fetching comments for event:', event_uqid, 'offset:', offset, 'limit:', limit);
      const response = await ApiGetComments(event_uqid, limit, offset);
      const comments = response.comments;
      const pagination = response.pagination;
      console.log('Received comments response:', response);
      console.log('Raw comments array:', comments);
      console.log('Pagination:', pagination);
      
      // Log the structure of the first comment to see all fields
      if (comments && comments.length > 0) {
        console.log('First comment raw object:', JSON.stringify(comments[0], null, 2));
        console.log('First comment keys:', Object.keys(comments[0]));
        console.log('First comment created_at:', comments[0].created_at);
      }
      
      // Ensure all comments have the created_at field
      const parsedComments = comments.map((comment: any) => ({
        id: comment.uqid,
        uqid: comment.event_uqid,
        user: comment.user,
        text: comment.text,
        created_at: comment.created_at || new Date().toISOString(),
        number_of_likes: comment.number_of_likes || 0
      }));
      
      console.log('Parsed comments:', parsedComments);
      
      // Update the selected event with fetched comments
      setSelectedEventForComments((prev) => {
        if (prev && prev.uqid === event_uqid) {
          // If we have an offset > 0, append comments; otherwise replace
          const updatedComments = offset > 0 && prev.comments 
            ? [...prev.comments, ...parsedComments]
            : parsedComments;
          console.log('Updated comments state:', updatedComments);
          return { ...prev, comments: updatedComments };
        }
        return prev;
      });
      
      // Also update the main events array so EventCard receives the comments
      setEvents((prevEvents) =>
        prevEvents.map((event) =>
          event.uqid === event_uqid
            ? {
                ...event,
                comments: offset > 0 && event.comments
                  ? [...event.comments, ...parsedComments]
                  : parsedComments,
              }
            : event
        )
      );
      
      // Update pagination state
      setCommentOffset(offset + limit);
      setCommentHasMore(pagination?.has_more || false);
      console.log('Updated offset to:', offset + limit, 'has_more:', pagination?.has_more);
    } catch (error) {
      console.error('Error fetching comments:', error);
    }
  };

  const handleAddComment = async (text: string, author: string) => {
    if (!selectedEventForComments) return;
    try {
      await ApiPost('event/comment', { 
        uqid: selectedEventForComments.uqid,
        user: author,
        text 
      });
      // Refresh comments for the current event (reset to offset 0)
      fetchCommentsForEvent(selectedEventForComments.uqid, 0);
    } catch (error) {
      console.error('Error adding comment:', error);
    }
  };

  const handleLikeComment = async (comment_id: string) => {
    try {
      console.log('Liking comment:', comment_id);
      await ApiLikeComment(comment_id);
      console.log('Comment liked successfully');
      // Refresh comments to update the like count
      if (selectedEventForComments) {
        console.log('Refreshing comments for event:', selectedEventForComments.uqid);
        fetchCommentsForEvent(selectedEventForComments.uqid);
      }
    } catch (error) {
      console.error('Error liking comment:', error);
    }
  };

  return (
    <div className="relative p-6">
      <Button 
        className="bg-[#970fff] text-white"
        onClick={() => {
          setNewEvent({});
          setIsDialogOpen(true);
        }}
      >
        Create New Event
      </Button>

      <EventDialog
        isOpen={isDialogOpen}
        onOpenChange={setIsDialogOpen}
        event={newEvent}
        onEventChange={setNewEvent}
        onSave={handleCreateOrUpdateEvent}
      />

      <EventComments
        isOpen={isCommentsOpen}
        onOpenChange={setIsCommentsOpen}
        event={selectedEventForComments}
        onAddComment={handleAddComment}
        hasMore={commentHasMore}
        onLoadMoreComments={() => {
          if (selectedEventForComments) {
            fetchCommentsForEvent(selectedEventForComments.uqid, commentOffset);
          }
        }}
        onLikeComment={handleLikeComment}
      />

      <div className="flex flex-col items-center mt-12">
        {isLoading ? (
          Array(3).fill(null).map((_, index) => <EventSkeleton key={index} />)
        ) : !events || events.length === 0 ? (
          <div>No events found.</div>
        ) : (
          events.map((event) => (
            <EventCard
              key={event.uqid}
              {...event}
              onLike={handleLikeEvent}
              onEdit={handleEditEvent}
              onViewComments={handleViewComments}
            />
          ))
        )}
      </div>
    </div>
  );
};

export default EventList;