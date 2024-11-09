import getAuthServerSession from "@/lib/get-auth-server-session";
import { redirect } from "next/navigation";
import { ReactNode } from "react";

export default async function Layout({ children }: { children: ReactNode }) {
  const session = await getAuthServerSession();
  console.log("session", session);
  if (!session) {
    return redirect("/login");
  }
  return children;
}
