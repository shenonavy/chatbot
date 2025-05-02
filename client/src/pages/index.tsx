import React, { KeyboardEvent, useEffect, useRef } from 'react';
import { ChatType } from '@/enum';
import { useChat } from '@/hook/use-chat';
import { IChatResponse } from '@/models';
import { Typewriter } from 'react-simple-typewriter';
import { SendHorizontal, Upload } from 'lucide-react';
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogFooter,
    DialogHeader,
    DialogTitle,
} from '@/components/atoms/dialog';
import { Uploader } from '@/components';

export default function Home() {
    const bottomRef = useRef<HTMLDivElement>(null);
    const { input, chats, isLoading, open, setOpen, setInput, onSubmit } = useChat();

    useEffect(() => {
        const container = bottomRef.current;
        if (container) {
            container.scrollTo({
                top: container.scrollHeight,
                behavior: 'smooth',
            });
        }
    }, [chats]);

    const handleKeyDown = (event: KeyboardEvent<HTMLInputElement>) => {
        if (event.key === 'Enter' && input?.trim() !== '') {
            onSubmit();
        }
    };

    return (
        <>
            <div ref={bottomRef} className="flex-1 overflow-y-auto p-4 space-y-4">
                {chats?.map((chat: IChatResponse, index: number) => (
                    <div
                        key={index}
                        className={`flex ${chat.type === ChatType.Agent ? 'justify-start' : 'justify-end'}`}
                    >
                        <div
                            className={`p-3 rounded-lg max-w-xs ${
                                chat.type === ChatType.Agent ? 'bg-gray-200 text-gray-900' : 'bg-blue-500 text-white'
                            }`}
                        >
                            <Typewriter words={[chat?.response ?? '']} loop={1} typeSpeed={20} />
                        </div>
                    </div>
                ))}

                {isLoading && (
                    <div id="typing-indicator" className="flex justify-start items-center space-x-2">
                        <span className="ml-1 text-sm text-gray-500">Bot is typing...</span>
                    </div>
                )}
            </div>

            <div className="p-4 bg-white flex items-center space-x-2">
                <input
                    type="text"
                    placeholder="Type your message..."
                    className="flex-1 p-2 border border-gray-300 rounded-md focus:outline-none focus:ring focus:border-blue-300"
                    value={input}
                    onInput={e => setInput(e.currentTarget.value)}
                    onKeyDown={handleKeyDown}
                />
                <div className="flex gap-2">
                    <button
                        disabled={isLoading}
                        className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
                        onClick={() => onSubmit()}
                    >
                        <SendHorizontal />
                    </button>
                    <button
                        disabled={isLoading}
                        className="bg-green-600 hover:bg-green-800 text-white px-4 py-2 rounded-md"
                        onClick={() => setOpen(true)}
                    >
                        <Upload />
                    </button>
                </div>
            </div>
            <Dialog open={open} onOpenChange={setOpen}>
                <DialogContent className="max-w-[unset] w-[580px]" onInteractOutside={event => event.preventDefault()}>
                    <DialogHeader className="px-0">
                        <DialogTitle asChild>
                            <div className="px-4 flex gap-2">
                                <p className="text-lg font-semibold text-gray-700">Upload your document</p>
                            </div>
                        </DialogTitle>
                    </DialogHeader>
                    <DialogDescription asChild>
                        <div className="px-4 flex flex-col gap-y-4 h-[351px] overflow-y-auto">
                            <Uploader />
                        </div>
                    </DialogDescription>
                    <DialogFooter>
                        <button
                            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
                            onClick={() => setOpen(true)}
                        >
                            Upload
                        </button>
                    </DialogFooter>
                </DialogContent>
            </Dialog>
        </>
    );
}
