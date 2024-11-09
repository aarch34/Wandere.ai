import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { AppRouterPageRoute, getSession, withPageAuthRequired } from '@auth0/nextjs-auth0';
import { Calendar, LogOut, Map, Plane, Settings, User } from "lucide-react";
import Image from 'next/image';
import Link from "next/link";
import { redirect } from "next/navigation";
import { ReactNode } from "react";
import Providers from "./providers";


const Layout = async ({ children }: { children: ReactNode }) => {
  const session = await getSession();
  if (!session?.user) {
    return redirect("/login");
  }
  return (
    <div className="h-screen flex">
      <div className="w-64 bg-teal-800 text-white p-6 flex flex-col">
        <div className="flex items-center gap-3 mb-8">
          <Plane size={24} className="text-teal-400" />
          <h1 className="text-2xl font-bold">Wandere.ai</h1>
        </div>

        <div className="mb-8 p-3 bg-teal-700/50 rounded-lg">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-teal-600 rounded-full flex items-center justify-center">
            <Avatar>
                <AvatarImage
                  src={session?.user?.image ?? "#"}
                  alt={session?.user?.name ?? "JD"}
                  asChild
                >
                  <Image
                    width={64}
                    height={64}
                    src={session?.user?.image ?? "#"}
                    alt={session?.user?.name ?? "JD"}
                  />
                </AvatarImage>
                <AvatarFallback>
                  {session?.user?.name?.slice(0, 2) ?? "JD"}
                </AvatarFallback>
              </Avatar>
            </div>
            <div>
              <h2 className="font-medium">{session.user?.name}</h2>
            </div>
          </div>
        </div>

        <nav className="flex-1">
          <ul className="space-y-4">
            <li>
              <button className="flex items-center gap-3 text-white/80 hover:text-white w-full p-2 rounded-lg hover:bg-teal-700 transition-colors">
                <Map size={20} />
                Explore
              </button>
            </li>
            <li>
              <Link
                href="/trips"
                className="flex items-center gap-3 text-white/80 hover:text-white w-full p-2 rounded-lg hover:bg-teal-700 transition-colors"
              >
                <Calendar size={20} />
                Trips
              </Link>
            </li>
            <li>
              <button className="flex items-center gap-3 text-white/80 hover:text-white w-full p-2 rounded-lg hover:bg-teal-700 transition-colors">
                <User size={20} />
                Profile
              </button>
            </li>
            <li>
              <button className="flex items-center gap-3 text-white/80 hover:text-white w-full p-2 rounded-lg hover:bg-teal-700 transition-colors">
                <Settings size={20} />
                Settings
              </button>
            </li>
          </ul>
        </nav>

        {/* Logout Button */}
        <a href="/api/auth/logout" className="flex items-center gap-3 text-white/80 hover:text-white w-full p-2 rounded-lg hover:bg-teal-700 transition-colors">
          <LogOut size={20} />
          Logout
        </a>
      </div>
      <Providers>{children}</Providers>
    </div>
  );
}

// See github issue https://github.com/auth0/nextjs-auth0/issues/1643 for more info
export default withPageAuthRequired(
  Layout as AppRouterPageRoute
, {
  returnTo: "/",
}) as React.FC;