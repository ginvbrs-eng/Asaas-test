"use client";

import { useOrganization } from "@/hooks/useOrganization";

export function OrgSwitcher() {
  const { activeOrgId, organizations, switchOrg } = useOrganization();

  return (
    <select
      className="w-full rounded border border-slate-300 bg-white px-3 py-2"
      value={activeOrgId ?? ""}
      onChange={(event) => switchOrg(Number(event.target.value))}
    >
      <option value="" disabled>
        Select organization
      </option>
      {organizations.map((org) => (
        <option key={org.id} value={org.id}>
          {org.name}
        </option>
      ))}
    </select>
  );
}
