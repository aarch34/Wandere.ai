import { authOptions } from "@/app/api/auth/[...nextauth]/auth-options";
import { getServerSession as gS } from "next-auth";
export default async function getAuthServerSession() {
  return await gS(authOptions);
}
