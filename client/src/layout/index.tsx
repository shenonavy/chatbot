import React from 'react';

export const Layout = ({ children }: { children: React.JSX.Element }) => {
    return (
        <div className="bg-gray-100 h-screen flex flex-col">
            <div className="bg-blue-600 text-white p-4 text-lg font-semibold">Chatbot Assistant</div>
            {children}
        </div>
    );
};

export default Layout;
