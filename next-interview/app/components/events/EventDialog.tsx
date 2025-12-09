import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogDescription, DialogFooter } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

interface IEventDialogProps {
  isOpen: boolean;
  onOpenChange: (open: boolean) => void;
  event: Partial<IEvent>;
  onEventChange: (event: Partial<IEvent>) => void;
  onSave: () => void;
}

interface IEvent {
  uqid: string;
  name: string;
  description: string;
  img_link: string;
  number_of_likes: number;
}

const EventDialog = (props: IEventDialogProps) => {
  const { isOpen, onOpenChange, event, onEventChange, onSave } = props;

  return (
    <Dialog open={isOpen} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>{event.uqid ? 'Edit Event' : 'Create New Event'}</DialogTitle>
          <DialogDescription>
            Fill in the details for your event.
          </DialogDescription>
        </DialogHeader>
        <div className="grid gap-4 py-4">
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="name" className="text-right">Name</Label>
            <Input
              id="name"
              value={event.name || ''}
              onChange={(e) => onEventChange({ ...event, name: e.target.value })}
              className="col-span-3 bg-gray-800 border-[#970fff] text-white"
            />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="description" className="text-right">Description</Label>
            <Input
              id="description"
              value={event.description || ''}
              onChange={(e) => onEventChange({ ...event, description: e.target.value })}
              className="col-span-3 bg-gray-800 border-[#970fff] text-white"
            />
          </div>
          <div className="grid grid-cols-4 items-center gap-4">
            <Label htmlFor="img_link" className="text-right">Image URL</Label>
            <Input
              id="img_link"
              value={event.img_link || ''}
              onChange={(e) => onEventChange({ ...event, img_link: e.target.value })}
              className="col-span-3 bg-gray-800 border-[#970fff] text-white"
            />
          </div>
        </div>
        <DialogFooter>
          <Button 
            onClick={onSave}
            disabled={!event.name || !event.description || !event.img_link}
            className="bg-[#970fff] text-white"
          >
            {event.uqid ? 'Update Event' : 'Create Event'}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default EventDialog; 