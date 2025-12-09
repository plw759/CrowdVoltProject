import { useState } from 'react';
import { useEffect } from 'react';
import { IEvent, IComment } from '@/app/types';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface EventCommentsProps {
  isOpen: boolean;
  onOpenChange: (open: boolean) => void;
  event: IEvent | null;
  cursor?: string | null;
  onAddComment: (text: string, author: string) => void;
  onLoadMoreComments?: (cursor: string | null) => void;
  onLikeComment?: (comment_id: string) => void;
}

const EventComments = (props: EventCommentsProps) => {
  const { isOpen, onOpenChange, event, cursor, onAddComment, onLoadMoreComments, onLikeComment } = props;
  const [newComment, setNewComment] = useState('');
  const [author, setAuthor] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isLoadingMore, setIsLoadingMore] = useState(false);
  const [likedComments, setLikedComments] = useState<Set<string>>(new Set());

  useEffect(() => {
    console.log('EventComments updated - event:', event);
    console.log('Comments array:', event?.comments);
    console.log('Comments length:', event?.comments?.length);
    if (event?.comments && event.comments.length > 0) {
      console.log('First comment:', JSON.stringify(event.comments[0], null, 2));
      console.log('First comment keys:', Object.keys(event.comments[0]));
      console.log('created_at field:', event.comments[0].created_at);
    }
  }, [event, event?.comments]);

  const handleSubmit = async () => {
    console.log('handleSubmit called - newComment:', newComment, 'author:', author);
    if (!newComment.trim() || !author.trim()) {
      console.log('Validation failed - missing comment or author');
      return;
    }
    setIsSubmitting(true);
    try {
      console.log('Calling onAddComment with:', { newComment, author });
      await onAddComment(newComment, author);
      console.log('onAddComment completed successfully');
      setNewComment('');
      setAuthor('');
    } catch (error) {
      console.error('Error in handleSubmit:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleLoadMore = async () => {
    if (!onLoadMoreComments) return;
    setIsLoadingMore(true);
    try {
      console.log('Loading more comments with composite cursor:', cursor);
      await onLoadMoreComments(cursor || null);
    } finally {
      setIsLoadingMore(false);
    }
  };

  const handleLikeComment = async (commentId: string) => {
    if (!onLikeComment) return;
    console.log('handleLikeComment called with commentId:', commentId);
    try {
      console.log('Calling onLikeComment callback');
      await onLikeComment(commentId);
      console.log('Like successful, updating local state');
      setLikedComments((prev) => new Set(prev).add(commentId));
    } catch (error) {
      console.error('Error liking comment:', error);
    }
  };

  if (!event) return null;

  return (
    <Dialog open={isOpen} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle>Comments on "{event.name}"</DialogTitle>
          <DialogDescription>
            View and add comments to this event
          </DialogDescription>
        </DialogHeader>

        <div className="max-h-96 overflow-y-auto py-4">
          {event.comments && event.comments.length > 0 ? (
            <div key="comments-list" className="space-y-3">
              {event.comments.map((comment) => (
                <div key={comment.id} className="bg-gray-800 p-3 rounded-lg">
                  <p className="text-[#970fff] text-sm font-semibold">{comment.user || 'Anonymous'}</p>
                  <p className="text-white text-sm mt-1">{comment.text}</p>
                  <div className="flex justify-between items-center mt-2">
                    <p className="text-gray-400 text-xs">
                      {comment.created_at 
                        ? new Date(comment.created_at).toLocaleDateString('en-US', {
                            year: 'numeric',
                            month: 'short',
                            day: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit'
                          })
                        : 'Unknown date'
                      }
                    </p>
                    {onLikeComment && (
                      <button
                        onClick={() => handleLikeComment(comment.id)}
                        disabled={likedComments.has(comment.id)}
                        className="flex items-center gap-1 px-2 py-1 rounded bg-blue-600 hover:bg-blue-700 text-white text-xs disabled:opacity-50 disabled:cursor-not-allowed"
                      >
                        👍 {comment.number_of_likes || 0}
                      </button>
                    )}
                  </div>
                </div>
              ))}
              {onLoadMoreComments && (
                <div key="load-more">
                  <button
                    onClick={handleLoadMore}
                    disabled={isLoadingMore}
                    className="w-full mt-4 py-2 px-4 bg-gray-700 hover:bg-gray-600 text-white rounded-lg text-sm disabled:opacity-50"
                  >
                    {isLoadingMore ? 'Loading...' : 'Load More Comments'}
                  </button>
                </div>
              )}
            </div>
          ) : (
            <div className="text-center text-gray-400 py-8">
              No comments yet. Be the first to comment!
            </div>
          )}
        </div>

        <DialogFooter>
          <div className="w-full space-y-2">
            <Input
              placeholder="Your name"
              value={author}
              onChange={(e) => setAuthor(e.target.value)}
              className="bg-gray-800 border-[#970fff] text-white"
            />
            <Input
              placeholder="Add a comment..."
              value={newComment}
              onChange={(e) => setNewComment(e.target.value)}
              className="bg-gray-800 border-[#970fff] text-white"
              onKeyPress={(e) => e.key === 'Enter' && handleSubmit()}
            />
            <Button
              onClick={handleSubmit}
              disabled={!newComment.trim() || !author.trim() || isSubmitting}
              className="w-full bg-[#970fff] text-white"
            >
              {isSubmitting ? 'Adding...' : 'Add Comment'}
            </Button>
          </div>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default EventComments;
