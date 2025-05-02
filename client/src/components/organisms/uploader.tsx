import Dropzone from 'react-dropzone';

export interface UploaderProps {
    files: File[];
    uploading: boolean;
    handleDrop: (acceptedFiles: File[]) => void;
    handleRemove: (fileToRemove: File) => void;
}

export const Uploader = (props: UploaderProps) => {
    const { files, uploading, handleDrop, handleRemove } = props;

    return (
        <div>
            <Dropzone
                onDrop={handleDrop}
                accept={{
                    'application/pdf': ['.pdf'],
                }}
            >
                {({ getRootProps, getInputProps }) => (
                    <section>
                        <div
                            {...getRootProps()}
                            className="h-[200px] border-2 border-dotted border-blue-500 rounded-md flex items-center justify-center text-center p-4"
                        >
                            <input {...getInputProps()} />
                            <p className="text-gray-600">Drag & drop some files here, or click to select files</p>
                        </div>
                    </section>
                )}
            </Dropzone>
            {files.length > 0 && (
                <ul className="space-y-2 mt-2">
                    {files.map((file, index) => (
                        <li key={index} className="flex justify-between items-center border p-2 rounded">
                            <span className="text-sm">{file.name}</span>
                            <button
                                disabled={uploading}
                                onClick={() => handleRemove(file)}
                                className="text-red-500 hover:text-red-700 text-sm"
                            >
                                Remove
                            </button>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default Uploader;
