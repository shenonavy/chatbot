import { ChatType } from '@/enum';

export interface IChatRequest {
    question: string;
}

export interface IChatResponse {
    status: string;
    response: string;
    type?: ChatType;
}
