"use client";

import { useEffect, useState } from "react";

import { useQuery } from "@tanstack/react-query";

export type Organization = {
  id: number;
  name: string;
};

export function useOrganization() {
  const [activeOrgId, setActiveOrgId] = useState<number | null>(null);

  const organizationsQuery = useQuery({
    queryKey: ["organizations"],
    queryFn: async (): Promise<Organization[]> => {
      // TODO: implement listUserOrgs() call.
      return [];
    },
  });

  useEffect(() => {
    const raw = localStorage.getItem("active_org_id");
    if (raw) {
      setActiveOrgId(Number(raw));
    }
  }, []);

  const switchOrg = (orgId: number) => {
    localStorage.setItem("active_org_id", String(orgId));
    setActiveOrgId(orgId);
  };

  return {
    activeOrgId,
    organizations: organizationsQuery.data ?? [],
    getCurrentOrg: () => activeOrgId,
    switchOrg,
    listUserOrgs: () => organizationsQuery.data ?? [],
  };
}
