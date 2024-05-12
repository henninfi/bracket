"use client"
import React, { useEffect, useContext } from 'react';
import { useAuthInfo } from "@propelauth/react";
import { OpenAPI } from '../../client/core/OpenAPI';

const AuthTokenUpdater = () => {
    const authInfo = useAuthInfo();

    // Check if the API URL is defined
    if (!process.env.NEXT_PUBLIC_API_RANKIT_URL) {
        throw new Error("API URL is not defined");
      }
    
    
    useEffect(() => {
        OpenAPI.BASE = process.env.NEXT_PUBLIC_API_RANKIT_URL as string;
        // Update the OpenAPI configuration with the new token
        // OpenAPI.TOKEN = authInfo.accessToken ? `Bearer ${authInfo.accessToken}` : '';
        
        // Alternatively, if you need to update headers directly:
        OpenAPI.HEADERS = {
            ...OpenAPI.HEADERS,
            Authorization: authInfo.accessToken ? `Bearer ${authInfo.accessToken}` : '',
        };
    }, [authInfo.accessToken]);
    console.log(OpenAPI)
    return null; // This component does not render anything
};

export default AuthTokenUpdater;
