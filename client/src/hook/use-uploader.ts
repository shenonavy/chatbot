import { useState } from 'react';

export const useUploader = () => {
    const [files, setFiles] = useState<File[]>([]);

    const handleDrop = (acceptedFiles: File[]) => {
        setFiles(prev => [...prev, ...acceptedFiles]);
    };

    const handleRemove = (fileToRemove: File) => {
        setFiles(prev => prev.filter(file => file !== fileToRemove));
    };

    return { files, handleDrop, handleRemove };
};
