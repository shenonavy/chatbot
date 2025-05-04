import { ChatType } from '@/enum';

export interface IChatRequest {
    question: string;
}

export interface IChatResponse {
    status: string;
    response: string;
    source_type?: ChatType;
}
