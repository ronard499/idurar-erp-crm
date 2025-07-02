import axios, { CancelTokenSource } from 'axios';
import { API_BASE_URL } from '@/config/serverApiConfig';
import { ApiResponse } from '@/types';

import errorHandler from './errorHandler';
import successHandler from './successHandler';
import storePersist from '@/redux/storePersist';
import {
  CreateRequest,
  ReadRequest,
  UpdateRequest,
  DeleteRequest,
  FilterRequest,
  SearchRequest,
  ListRequest,
  PostRequest,
  GetRequest,
  PatchRequest,
  UploadRequest,
  ConvertRequest,
  MailRequest,
} from './types';

/**
 * Find a key in an object that starts with a given prefix
 * @param object - The object to search in
 * @param prefix - The prefix to search for
 * @returns The key that starts with the prefix, or undefined if not found
 */
function findKeyByPrefix(object: Record<string, any>, prefix: string): string | undefined {
  for (const property in object) {
    if (
      Object.prototype.hasOwnProperty.call(object, property) &&
      property.toString().startsWith(prefix)
    ) {
      return property;
    }
  }
  return undefined;
}

/**
 * Include the authentication token in the request headers
 */
function includeToken(): void {
  axios.defaults.baseURL = API_BASE_URL;
  axios.defaults.withCredentials = true;
  
  const auth = storePersist.get('auth');

  if (auth && auth.current && auth.current.token) {
    axios.defaults.headers.common['Authorization'] = `Bearer ${auth.current.token}`;
  }
}

/**
 * Request object containing methods for API requests
 */
const request = {
  /**
   * Create a new resource
   * @param param0 - Object containing entity and jsonData
   * @returns API response
   */
  create: async <T = any, R = any>({ entity, jsonData }: CreateRequest<T>): Promise<ApiResponse<R>> => {
    try {
      includeToken();
      const response = await axios.post(`${entity}/create`, jsonData);
      successHandler(response, {
        notifyOnSuccess: true,
        notifyOnFailed: true,
      });
      return response.data;
    } catch (error) {
      return errorHandler(error);
    }
  },

  /**
   * Create a new resource with file upload
   * @param param0 - Object containing entity and jsonData (FormData)
   * @returns API response
   */
  createAndUpload: async <T = FormData, R = any>({ entity, jsonData }: CreateRequest<T>): Promise<ApiResponse<R>> => {
    try {
      includeToken();
      const response = await axios.post(`${entity}/create`, jsonData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      successHandler(response, {
        notifyOnSuccess: true,
        notifyOnFailed: true,
      });
      return response.data;
    } catch (error) {
      return errorHandler(error);
    }
  },

  /**
   * Read a resource by ID
   * @param param0 - Object containing entity and id
   * @returns API response
   */
  read: async <R = any>({ entity, id }: ReadRequest): Promise<ApiResponse<R>> => {
    try {
      includeToken();
      const response = await axios.get(`${entity}/read/${id}`);
      successHandler(response, {
        notifyOnSuccess: false,
        notifyOnFailed: true,
      });
      return response.data;
    } catch (error) {
      return errorHandler(error);
    }
  },

  /**
   * Update a resource by ID
   * @param param0 - Object containing entity, id, and jsonData
   * @returns API response
   */
  update: async <T = any, R = any>({ entity, id, jsonData }: UpdateRequest<T>): Promise<ApiResponse<R>> => {
    try {
      includeToken();
      const response = await axios.patch(`${entity}/update/${id}`, jsonData);
      successHandler(response, {
        notifyOnSuccess: true,
        notifyOnFailed: true,
      });
      return response.data;
    } catch (error) {
      return errorHandler(error);
    }
  },

  /**
   * Update a resource with file upload
   * @param param0 - Object containing entity, id, and jsonData (FormData)
   * @returns API response
   */
  updateAndUpload: async <T = FormData, R = any>({ entity, id, jsonData }: UpdateRequest<T>): Promise<ApiResponse<R>> => {
    try {
      includeToken();
      const response = await axios.patch(`${entity}/update/${id}`, jsonData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      successHandler(response, {
        notifyOnSuccess: true,
        notifyOnFailed: true,
      });
      return response.data;
    } catch (error) {
      return errorHandler(error);
    }
  },

  /**
   * Delete a resource by ID
   * @param param0 - Object containing entity and id
   * @returns API response
   */
  delete: async <R = any>({ entity, id }: DeleteRequest): Promise<ApiResponse<R>> => {
    try {
      includeToken();
      const response = await axios.delete(`${entity}/delete/${id}`);
      successHandler(response, {
        notifyOnSuccess: true,
        notifyOnFailed: true,
      });
      return response.data;
    } catch (error) {
      return errorHandler(error);
    }
  },

  /**
   * Filter resources
   * @param param0 - Object containing entity and options
   * @returns API response
   */
  filter: async <R = any>({ entity, options = {} }: FilterRequest): Promise<ApiResponse<R>> => {
    try {
      includeToken();
      const filter = options.filter ? `filter=${options.filter}` : '';
      const equal = options.equal ? `&equal=${options.equal}` : '';
      const query = `?${filter}${equal}`;

      const response = await axios.get(`${entity}/filter${query}`);
      successHandler(response, {
        notifyOnSuccess: false,
        notifyOnFailed: false,
      });
      return response.data;
    } catch (error) {
      return errorHandler(error);
    }
  },

  /**
   * Search resources
   * @param param0 - Object containing entity and options
   * @returns API response
   */
  search: async <R = any>({ entity, options = {} }: SearchRequest): Promise<ApiResponse<R>> => {
    try {
      includeToken();
      let query = '?';
      for (const key in options) {
        if (Object.prototype.hasOwnProperty.call(options, key)) {
          query += `${key}=${options[key]}&`;
        }
      }
      query = query.slice(0, -1);
      
      const response = await axios.get(`${entity}/search${query}`);

      successHandler(response, {
        notifyOnSuccess: false,
        notifyOnFailed: false,
      });
      return response.data;
    } catch (error) {
      return errorHandler(error);
    }
  },

  /**
   * List resources with pagination
   * @param param0 - Object containing entity and options
   * @returns API response
   */
  list: async <R = any>({ entity, options = {} }: ListRequest): Promise<ApiResponse<R>> => {
    try {
      includeToken();
      let query = '?';
      for (const key in options) {
        if (Object.prototype.hasOwnProperty.call(options, key)) {
          query += `${key}=${options[key]}&`;
        }
      }
      query = query.slice(0, -1);

      const response = await axios.get(`${entity}/list${query}`);

      successHandler(response, {
        notifyOnSuccess: false,
        notifyOnFailed: false,
      });
      return response.data;
    } catch (error) {
      return errorHandler(error);
    }
  },

  /**
   * List all resources without pagination
   * @param param0 - Object containing entity and options
   * @returns API response
   */
  listAll: async <R = any>({ entity, options = {} }: ListRequest): Promise<ApiResponse<R>> => {
    try {
      includeToken();
      let query = '?';
      for (const key in options) {
        if (Object.prototype.hasOwnProperty.call(options, key)) {
          query += `${key}=${options[key]}&`;
        }
      }
      query = query.slice(0, -1);

      const response = await axios.get(`${entity}/listAll${query}`);

      successHandler(response, {
        notifyOnSuccess: false,
        notifyOnFailed: false,
      });
      return response.data;
    } catch (error) {
      return errorHandler(error);
    }
  },

  /**
   * Generic POST request
   * @param param0 - Object containing entity and jsonData
   * @returns API response
   */
  post: async <T = any, R = any>({ entity, jsonData }: PostRequest<T>): Promise<ApiResponse<R>> => {
    try {
      includeToken();
      const response = await axios.post(entity, jsonData);
      return response.data;
    } catch (error) {
      return errorHandler(error);
    }
  },

  /**
   * Generic GET request
   * @param param0 - Object containing entity
   * @returns API response
   */
  get: async <R = any>({ entity }: GetRequest): Promise<ApiResponse<R>> => {
    try {
      includeToken();
      const response = await axios.get(entity);
      return response.data;
    } catch (error) {
      return errorHandler(error);
    }
  },

  /**
   * Generic PATCH request
   * @param param0 - Object containing entity and jsonData
   * @returns API response
   */
  patch: async <T = any, R = any>({ entity, jsonData }: PatchRequest<T>): Promise<ApiResponse<R>> => {
    try {
      includeToken();
      const response = await axios.patch(entity, jsonData);
      successHandler(response, {
        notifyOnSuccess: true,
        notifyOnFailed: true,
      });
      return response.data;
    } catch (error) {
      return errorHandler(error);
    }
  },

  /**
   * Upload a file
   * @param param0 - Object containing entity, id, and jsonData (FormData)
   * @returns API response
   */
  upload: async <T = FormData, R = any>({ entity, id, jsonData }: UploadRequest<T>): Promise<ApiResponse<R>> => {
    try {
      includeToken();
      const response = await axios.patch(`${entity}/upload/${id}`, jsonData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      successHandler(response, {
        notifyOnSuccess: true,
        notifyOnFailed: true,
      });
      return response.data;
    } catch (error) {
      return errorHandler(error);
    }
  },

  /**
   * Create a cancel token source
   * @returns CancelTokenSource
   */
  source: (): CancelTokenSource => {
    const CancelToken = axios.CancelToken;
    const source = CancelToken.source();
    return source;
  },

  /**
   * Get summary data
   * @param param0 - Object containing entity and options
   * @returns API response
   */
  summary: async <R = any>({ entity, options = {} }: ListRequest): Promise<ApiResponse<R>> => {
    try {
      includeToken();
      let query = '?';
      for (const key in options) {
        if (Object.prototype.hasOwnProperty.call(options, key)) {
          query += `${key}=${options[key]}&`;
        }
      }
      query = query.slice(0, -1);
      const response = await axios.get(`${entity}/summary${query}`);

      successHandler(response, {
        notifyOnSuccess: false,
        notifyOnFailed: false,
      });

      return response.data;
    } catch (error) {
      return errorHandler(error);
    }
  },

  /**
   * Send an email
   * @param param0 - Object containing entity and jsonData
   * @returns API response
   */
  mail: async <T = any, R = any>({ entity, jsonData }: MailRequest<T>): Promise<ApiResponse<R>> => {
    try {
      includeToken();
      const response = await axios.post(`${entity}/mail/`, jsonData);
      successHandler(response, {
        notifyOnSuccess: true,
        notifyOnFailed: true,
      });
      return response.data;
    } catch (error) {
      return errorHandler(error);
    }
  },

  /**
   * Convert a resource
   * @param param0 - Object containing entity and id
   * @returns API response
   */
  convert: async <R = any>({ entity, id }: ConvertRequest): Promise<ApiResponse<R>> => {
    try {
      includeToken();
      const response = await axios.get(`${entity}/convert/${id}`);
      successHandler(response, {
        notifyOnSuccess: true,
        notifyOnFailed: true,
      });
      return response.data;
    } catch (error) {
      return errorHandler(error);
    }
  },
};
export default request;
