import { useState, useCallback } from 'react';
import { BookingRequest, BookingStatus, WorkflowStatus } from '@/types';
import { bookingService } from '@/services/bookingService';
import { usePolling } from './usePolling';
import { STATUS } from '@/utils/status';

export const useBooking = () => {
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [requestId, setRequestId] = useState<string | null>(null);
  
  // Workflow state
  const [status, setStatus] = useState<WorkflowStatus | null>(null);
  const [result, setResult] = useState<BookingStatus['result']>();
  const [errors, setErrors] = useState<string[]>([]);

  // Polling control: poll if we have a request ID and the status is QUEUED or RUNNING
  const shouldPoll = !!requestId && (status === STATUS.QUEUED || status === STATUS.RUNNING);

  const fetchStatus = useCallback(async () => {
    if (!requestId) return;
    try {
      const data = await bookingService.getBookingStatus(requestId);
      setStatus(data.status);
      
      if (data.status === STATUS.COMPLETED || data.status === STATUS.FAILED) {
        setResult(data.result);
        setErrors(data.errors || []);
      }
    } catch (err) {
      console.error('Failed to fetch booking status', err);
      // We don't automatically stop polling on a single network error, 
      // but you could set an error state here if desired.
    }
  }, [requestId]);

  usePolling(fetchStatus, 1000, shouldPoll);

  const submitBooking = async (request: BookingRequest) => {
    setIsSubmitting(true);
    setErrors([]);
    setResult(undefined);
    setStatus(null);
    setRequestId(null);

    try {
      const data = await bookingService.submitBooking(request);
      setRequestId(data.request_id);
      setStatus(data.status as WorkflowStatus);
    } catch (err: any) {
      setErrors([err?.message || 'Failed to submit booking request.']);
      setStatus(STATUS.FAILED);
    } finally {
      setIsSubmitting(false);
    }
  };

  const reset = () => {
    setRequestId(null);
    setStatus(null);
    setResult(undefined);
    setErrors([]);
  };

  return {
    submitBooking,
    reset,
    isSubmitting,
    status,
    result,
    errors,
    requestId,
  };
};
