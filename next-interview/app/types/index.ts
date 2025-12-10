export interface IComment {
  id: string;
  uqid: string;
  user: string;
  text: string;
  created_at: string;
  number_of_likes?: number;
}

export interface IEvent {
  uqid: string;
  name: string;
  description: string;
  img_link: string;
  number_of_likes: number;
  comments: IComment[];
  total_comments?: number;
}
