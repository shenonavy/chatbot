import { ChatType } from '@/enum';
import { IChatRequest, IChatResponse } from '@/models';
import { useState } from 'react';
import { useMutation } from 'react-query';

const executeChat = async (req: IChatRequest) => {
    try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_CHATBOT_BASE_URL}/chatbot`, {
            method: 'POST',
            body: JSON.stringify(req),
            headers: {
                'Content-Type': 'application/json',
            },
        });
        return (await response.json()) as IChatResponse;
    } catch (error) {
        console.error('Error occurred while executing chat:', error);
        throw error;
    }
};

export const useChat = () => {
    const [chats, setChat] = useState<IChatResponse[]>([]);
    const [input, setInput] = useState<string>('');
    const [open, setOpen] = useState<boolean>(false);

    const { mutate, isLoading } = useMutation((data: IChatRequest) => executeChat(data), {
        onSuccess: response => {
            setChat(prev => [...prev, { type: ChatType.Agent, ...response }]);
        },
        onError: (error: unknown) => {
            console.error('Error occurred while executing chat:', error);
        },
    });

    const onSubmit = () => {
        setChat(prev => [...prev, { type: ChatType.Human, response: input, status: 'success' }]);
        mutate({ question: input });
        setInput('');
    };

    return {
        isLoading,
        chats,
        input,
        open,
        setOpen,
        setInput,
        onSubmit,
    };
};
