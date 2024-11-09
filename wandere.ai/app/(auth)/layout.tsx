import { AppRouterPageRoute, getSession, withPageAuthRequired } from "@auth0/nextjs-auth0";
import { redirect } from "next/navigation";
import { ReactNode } from "react";

const Layout = async ({ children }: { children: ReactNode }) => {
  const session = await getSession();
  if (session?.user) {
    return redirect("/dashboard");
  }
  return <>{children}</>;
}

// See github issue https://github.com/auth0/nextjs-auth0/issues/1643 for more info
export default withPageAuthRequired(
  Layout as AppRouterPageRoute
, {
  returnTo: "/",
}) as React.FC;