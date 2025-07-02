import { AxiosResponse } from 'axios';
import { ApiResponse } from '@/types';

export interface RequestOptions {
  [key: string]: string | number | boolean;
}

export interface RequestHandlerOptions {
  notifyOnSuccess?: boolean;
  notifyOnFailed?: boolean;
}

export interface CreateRequest<T = any> {
  entity: string;
  jsonData: T;
}

export interface ReadRequest {
  entity: string;
  id: string;
}

export interface UpdateRequest<T = any> {
  entity: string;
  id: string;
  jsonData: T;
}

export interface DeleteRequest {
  entity: string;
  id: string;
}

export interface FilterRequest {
  entity: string;
  options?: {
    filter?: string;
    equal?: string;
    [key: string]: any;
  };
}

export interface SearchRequest {
  entity: string;
  options?: RequestOptions;
}

export interface ListRequest {
  entity: string;
  options?: RequestOptions;
}

export interface PostRequest<T = any> {
  entity: string;
  jsonData: T;
}

export interface GetRequest {
  entity: string;
}

export interface PatchRequest<T = any> {
  entity: string;
  jsonData: T;
}

export interface UploadRequest<T = any> {
  entity: string;
  id: string;
  jsonData: T;
}

export interface ConvertRequest {
  entity: string;
  id: string;
}

export interface MailRequest<T = any> {
  entity: string;
  jsonData: T;
}

export interface SuccessHandlerParams {
  data: ApiResponse;
  status: number;
  statusText: string;
  headers: any;
  config: any;
}

export type ErrorHandlerParams = any;