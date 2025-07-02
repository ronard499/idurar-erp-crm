/**
 * Server API configuration
 * Contains all the API endpoints and configuration for the application
 */

// API base URL for all API requests
export const API_BASE_URL: string =
  import.meta.env.PROD || import.meta.env.VITE_DEV_REMOTE === 'remote'
    ? `${import.meta.env.VITE_BACKEND_SERVER}api/`
    : 'https://work-1-hoawaswwbhuszcua.prod-runtime.all-hands.dev:12010/api/auth/';

// Base URL for the backend server
export const BASE_URL: string =
  import.meta.env.PROD || import.meta.env.VITE_DEV_REMOTE
    ? import.meta.env.VITE_BACKEND_SERVER as string
    : 'https://work-1-hoawaswwbhuszcua.prod-runtime.all-hands.dev:12010/';

// Website URL for the frontend
export const WEBSITE_URL: string = import.meta.env.PROD
  ? 'http://cloud.idurarapp.com/'
  : 'http://localhost:12014/';

// Base URL for downloading files
export const DOWNLOAD_BASE_URL: string =
  import.meta.env.PROD || import.meta.env.VITE_DEV_REMOTE
    ? `${import.meta.env.VITE_BACKEND_SERVER}media/`
    : 'https://work-1-hoawaswwbhuszcua.prod-runtime.all-hands.dev/media/';

// Name of the access token stored in localStorage
export const ACCESS_TOKEN_NAME: string = 'x-auth-token';

// Base URL for file uploads
export const FILE_BASE_URL: string = import.meta.env.VITE_FILE_BASE_URL as string;
