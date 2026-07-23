/**
 * Custom hook for interacting with a generic agentic workflow.
 * Empty implementation for Sprint 1.
 */
export const useWorkflow = () => {
  return {
    status: 'QUEUED',
    startWorkflow: async () => {},
    cancelWorkflow: async () => {},
  };
};
