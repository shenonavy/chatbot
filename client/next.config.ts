import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  reactStrictMode: true,
  env: {
    NEXT_PUBLIC_CHATBOT_BASE_URL: process.env.NEXT_PUBLIC_CHATBOT_BASE_URL,
  },
};

export default nextConfig;
