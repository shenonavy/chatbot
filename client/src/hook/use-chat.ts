import { ChatType } from '@/enum';
import { IChatRequest, IChatResponse } from '@/models';
import { useState } from 'react';
import { useMutation } from 'react-query';

const executeChat = async (req: IChatRequest) => {
    try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_CHATBOT_BASE_URL}/rag`, {
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

const uploadDocs = async (formData: FormData) => {
    try {
        const response = await fetch(`${process.env.NEXT_PUBLIC_CHATBOT_BASE_URL}/upload`, {
            method: 'POST',
            body: formData,
        });
        return await response.json();
    } catch (error) {
        console.error('Error occurred while uploading docs:', error);
        throw error;
    }
};

export const useChat = () => {
    const [chats, setChat] = useState<IChatResponse[]>([]);
    const [input, setInput] = useState<string>('');
    const [open, setOpen] = useState<boolean>(false);
    const [files, setFiles] = useState<File[]>([]);

    const handleDrop = (acceptedFiles: File[]) => {
        setFiles(prev => [...prev, ...acceptedFiles]);
    };

    const handleRemove = (fileToRemove: File) => {
        setFiles(prev => prev.filter(file => file !== fileToRemove));
    };

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

    const { mutate: mutateUpload, isLoading: uploading } = useMutation((formData: FormData) => uploadDocs(formData), {
        onSuccess: () => {
            setFiles([]);
            setOpen(false);
        },
        onError: (error: unknown) => {
            console.error('Error occurred while uploading docs:', error);
        },
    });

    const handleUpload = async () => {
        const formData = new FormData();
        files.forEach(file => {
            formData.append('files', file);
        });
        mutateUpload(formData);
    };

    return {
        isLoading,
        uploading,
        chats,
        input,
        open,
        files,
        setOpen,
        setInput,
        onSubmit,
        handleUpload,
        handleDrop,
        handleRemove,
    };
};
