import Image from 'next/image';
import { IEvent, IComment } from '@/app/types';
import { Button } from "@/components/ui/button";

interface IEventCardProps {
  name: string;
  description: string;
  img_link: string;
  number_of_likes: number;
  uqid: string;
  onLike: (uqid: string) => void;
  onEdit: (event: IEvent) => void;
  onViewComments: (event: IEvent) => void;
  comments: IComment[];
}

const EventCard = (props: IEventCardProps) => {
  const { name, description, img_link, number_of_likes, uqid, onLike, onEdit, onViewComments, comments } = props;
  
  return (
    <div className="w-full max-w-md mb-6">
      <div className="relative w-full rounded-xl overflow-hidden" style={{ paddingTop: "56.25%" }}>
        <Image
          src={img_link}
          alt={name}
          fill
          style={{ objectFit: "cover" }}
          className="rounded-xl border border-gray-500"
        />
      </div>
      <div className="mt-2">
        <h3 className="font-bold text-lg">{name}</h3>
        <p className="text-sm text-white text-opacity-60">{description}</p>
        <div className="flex justify-between items-center mt-2">
          <Button
            onClick={() => onLike(uqid)}
            className="bg-blue-500 text-white"
            aria-label={`Like event: ${name}`}
          >
            Like ({number_of_likes})
          </Button>
          <Button
            onClick={() => onViewComments({ uqid, name, description, img_link, number_of_likes, comments })}
            className="bg-orange-500 text-white"
          >
            Comments ({comments.length})
          </Button>
          <Button
            onClick={() => onEdit({ uqid, name, description, img_link, number_of_likes, comments })}
            className="bg-green-500 text-white"
          >
            Edit
          </Button>
        </div>
      </div>
    </div>
  );
};

export default EventCard; 