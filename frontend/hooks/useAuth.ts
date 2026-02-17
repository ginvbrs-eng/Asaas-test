"use client";

import { useQuery } from "@tanstack/react-query";

export function useAuth() {
  const sessionQuery = useQuery({
    queryKey: ["session"],
    queryFn: async () => {
      // TODO: call backend profile endpoint.
      return null;
    },
  });

  return {
    sessionQuery,
    isAuthenticated: Boolean(sessionQuery.data),
  };
}
