import { BookingRequest, BookingStatus } from '@/types';
import { apiClient } from '@/api/client';
import { API_ENDPOINTS } from '@/utils/api';

/**
 * Service for interacting with Booking APIs.
 */
export const bookingService = {
  submitBooking: async (request: BookingRequest): Promise<{ request_id: string; status: string }> => {
    const response = await apiClient.post(API_ENDPOINTS.BOOKINGS, request);
    return response.data;
  },

  getBookingStatus: async (requestId: string): Promise<BookingStatus> => {
    const response = await apiClient.get(`${API_ENDPOINTS.BOOKINGS}/${requestId}`);
    return response.data;
  },

  cancelBooking: async (requestId: string): Promise<void> => {
    // Backend doesn't support cancel yet, but interface is prepared
    console.warn(`Cancel booking ${requestId} not implemented on backend.`);
  }
};
