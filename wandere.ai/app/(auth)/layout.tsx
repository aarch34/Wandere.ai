import getAuthServerSession from "@/lib/get-auth-server-session";
import { redirect } from "next/navigation";

export default async function Layout({ children }) {
  const session = await getAuthServerSession();
  if (session) {
    return redirect("/dashboard");
  }
  return <>{children}</>;
}
