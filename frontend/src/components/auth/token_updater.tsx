"use client"
import { useEffect } from 'react';
import { useAuthInfo } from "@propelauth/react";
import { OpenAPI } from '../../client/core/OpenAPI';

const AuthTokenUpdater = () => {
    const authInfo = useAuthInfo();

    // Check if the API URL is defined
    if (!process.env.NEXT_PUBLIC_API_RANKIT_URL) {
        throw new Error("API URL is not defined");
      }
    OpenAPI.BASE = process.env.NEXT_PUBLIC_API_RANKIT_URL as string;
    OpenAPI.HEADERS = {
        ...OpenAPI.HEADERS,
        Authorization: `Bearer ${authInfo.accessToken}`,
    };
    // When authInfo.
    useEffect(() => {
        OpenAPI.BASE = process.env.NEXT_PUBLIC_API_RANKIT_URL as string;
        // Update the OpenAPI configuration with the new token
        OpenAPI.HEADERS = {
            ...OpenAPI.HEADERS,
            Authorization: `Bearer ${authInfo.accessToken}`,
        };
    }, [authInfo.isLoggedIn]);
    return null; // This component does not render anything
};

export default AuthTokenUpdater;
