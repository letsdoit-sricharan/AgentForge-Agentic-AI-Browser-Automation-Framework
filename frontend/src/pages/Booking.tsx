import React, { useState } from 'react';
import { PageContainer } from '@/components/common/PageContainer';
import { Card } from '@/components/common/Card';
import { Button } from '@/components/common/Button';
import { Input } from '@/components/common/Input';
import { Loader } from '@/components/common/Loader';
import { StatusBadge } from '@/components/common/StatusBadge';
import { useBooking } from '@/hooks/useBooking';
import { STATUS } from '@/utils/status';
import { useExecutionEvents } from '@/hooks/useExecutionEvents';
import { WorkflowTimeline } from '@/components/booking/WorkflowTimeline';
import { ResultCard } from '@/components/booking/ResultCard';
import { ErrorCard } from '@/components/booking/ErrorCard';

export const Booking: React.FC = () => {
  const { submitBooking, reset, isSubmitting, status, result, errors, requestId } = useBooking();
  const { events, isSubscribed, error: eventError } = useExecutionEvents(requestId);

  const [formData, setFormData] = useState({
    movie: '',
    city: '',
    show_date: '',
    preferred_theatre: '',
    preferred_time: '',
    seat_preference: '',
    ticket_count: 1,
  });

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'ticket_count' ? parseInt(value) || 1 : value
    }));
  };

  // Required validation
  const isValid = 
    formData.movie.trim() !== '' && 
    formData.city.trim() !== '' && 
    formData.show_date.trim() !== '' && 
    formData.ticket_count >= 1 && 
    formData.ticket_count <= 10;

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!isValid) return;

    submitBooking({
      movie: formData.movie,
      city: formData.city,
      show_date: formData.show_date,
      preferred_theatre: formData.preferred_theatre || undefined,
      preferred_time: formData.preferred_time || undefined,
      seat_preference: formData.seat_preference || undefined,
      ticket_count: formData.ticket_count,
    });
  };

  const isWorking = isSubmitting || status === STATUS.QUEUED || status === STATUS.RUNNING;
  const showForm = status === null;

  return (
    <PageContainer title="BookMyShow Integration">
      
      <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-lg)' }}>
        
        {/* Header with Status */}
        {status && (
          <div style={{ display: 'flex', justifyContent: 'flex-end', alignItems: 'center', gap: 'var(--spacing-sm)' }}>
            <span style={{ fontWeight: 'bold' }}>Current Status:</span>
            <StatusBadge status={status} />
          </div>
        )}

        {/* Input Form (Visible initially) */}
        {showForm && (
          <Card title="New Booking Request">
            <form onSubmit={handleSubmit}>
              <fieldset disabled={isWorking} style={{ border: 'none', padding: 0, margin: 0 }}>
                <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0 var(--spacing-md)' }}>
                  <Input 
                    label="Movie Name *" 
                    name="movie" 
                    value={formData.movie} 
                    onChange={handleChange} 
                    placeholder="e.g. Deadpool & Wolverine" 
                    required 
                  />
                  <Input 
                    label="City *" 
                    name="city" 
                    value={formData.city} 
                    onChange={handleChange} 
                    placeholder="e.g. Mumbai" 
                    required 
                  />
                  <Input 
                    label="Show Date *" 
                    name="show_date" 
                    type="date" 
                    value={formData.show_date} 
                    onChange={handleChange} 
                    required 
                  />
                  <Input 
                    label="Tickets *" 
                    name="ticket_count" 
                    type="number" 
                    min="1" 
                    max="10" 
                    value={formData.ticket_count} 
                    onChange={handleChange} 
                    required 
                  />
                  <Input 
                    label="Preferred Theatre (Optional)" 
                    name="preferred_theatre" 
                    value={formData.preferred_theatre} 
                    onChange={handleChange} 
                    placeholder="e.g. PVR Phoenix" 
                  />
                  <Input 
                    label="Preferred Time (Optional)" 
                    name="preferred_time" 
                    value={formData.preferred_time} 
                    onChange={handleChange} 
                    placeholder="e.g. 07:30 PM" 
                  />
                  <Input 
                    label="Seat Preference (Optional)" 
                    name="seat_preference" 
                    value={formData.seat_preference} 
                    onChange={handleChange} 
                    placeholder="e.g. any, rear, middle" 
                  />
                </div>
                
                <div style={{ marginTop: 'var(--spacing-md)' }}>
                  <Button type="submit" disabled={!isValid || isWorking} isLoading={isWorking}>
                    {isWorking ? 'Submitting...' : 'Execute Booking'}
                  </Button>
                </div>
              </fieldset>
            </form>
          </Card>
        )}

        {/* Loading Experience & Workflow Timeline */}
        {isWorking && (
          <Card title="Agent Execution">
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', padding: 'var(--spacing-xl) 0' }}>
              <Loader size="lg" text="Agent is executing booking workflow in browser..." />
              
              <div style={{ width: '100%', maxWidth: '400px', marginTop: 'var(--spacing-xl)' }}>
                <WorkflowTimeline status={status} events={events} isSubscribed={isSubscribed} error={eventError} />
              </div>
            </div>
          </Card>
        )}

        {/* Success Output */}
        {status === STATUS.COMPLETED && result && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-lg)' }}>
            <ResultCard result={result} />
            
            <Card title="Workflow Review">
              <WorkflowTimeline status={status} events={events} isSubscribed={isSubscribed} error={eventError} />
              <div style={{ marginTop: 'var(--spacing-lg)', borderTop: '1px solid var(--color-border)', paddingTop: 'var(--spacing-md)' }}>
                <Button variant="outline" onClick={reset}>Make Another Booking</Button>
              </div>
            </Card>
          </div>
        )}

        {/* Failure Output */}
        {status === STATUS.FAILED && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 'var(--spacing-lg)' }}>
            <ErrorCard errors={errors} onRetry={reset} />
            <Card>
              <WorkflowTimeline status={status} events={events} isSubscribed={isSubscribed} error={eventError} />
            </Card>
          </div>
        )}

      </div>
    </PageContainer>
  );
};
