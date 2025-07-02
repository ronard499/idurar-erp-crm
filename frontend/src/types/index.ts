// Common types used throughout the application

export interface User {
  id: string;
  name: string;
  surname: string;
  email: string;
  photo?: string | null;
  enabled: boolean;
  created: string;
  updated: string;
}

export interface AuthState {
  current: User | null;
  isLoggedIn: boolean;
  isLoading: boolean;
  error: string | null;
}

export interface ApiResponse<T = any> {
  success: boolean;
  result?: T;
  message?: string;
  error?: string;
}

export interface PaginatedResponse<T = any> {
  success: boolean;
  result: {
    items: T[];
    totalItems: number;
    currentPage: number;
    totalPages: number;
  };
  message?: string;
}

export interface Customer {
  id: string;
  name: string;
  email: string;
  phone?: string;
  address?: string;
  company?: string;
  created: string;
  updated: string;
}

export interface Product {
  id: string;
  name: string;
  description?: string;
  price: number;
  created: string;
  updated: string;
}

export interface Invoice {
  id: string;
  number: string;
  customer: string | Customer;
  date: string;
  expiredDate: string;
  items: InvoiceItem[];
  status: string;
  total: number;
  created: string;
  updated: string;
}

export interface InvoiceItem {
  id: string;
  product: string | Product;
  quantity: number;
  price: number;
  total: number;
}

export interface Quote {
  id: string;
  number: string;
  customer: string | Customer;
  date: string;
  expiredDate: string;
  items: QuoteItem[];
  status: string;
  total: number;
  created: string;
  updated: string;
}

export interface QuoteItem {
  id: string;
  product: string | Product;
  quantity: number;
  price: number;
  total: number;
}

export interface Payment {
  id: string;
  number: string;
  customer: string | Customer;
  invoice: string | Invoice;
  amount: number;
  date: string;
  method: string;
  status: string;
  created: string;
  updated: string;
}

export interface Supplier {
  id: string;
  name: string;
  email: string;
  phone?: string;
  address?: string;
  company?: string;
  created: string;
  updated: string;
}

export interface AppSettings {
  id: string;
  company_name: string;
  company_email: string;
  company_phone?: string;
  company_address?: string;
  company_website?: string;
  company_logo?: string;
  currency: string;
  created: string;
  updated: string;
}

export interface ReduxAction<T = any> {
  type: string;
  payload?: T;
  error?: boolean;
  meta?: any;
}

export interface ReduxState {
  auth: AuthState;
  // Add other state slices as needed
}