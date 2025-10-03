export type Role = "user" | "assistant";


export type Message = {
id?: number;
conversation_id?: number;
sender: Role;
content: string;
created_at?: string | null;
partial?: boolean;
};


export type Conversation = {
id: number;
title: string;
created_at?: string | null;
};
