import getAuthServerSession from "@/lib/get-auth-server-session";
import { Calendar, LogOut, Map, Plane, Settings, User } from "lucide-react";
import Link from "next/link";
import { redirect } from "next/navigation";
import { ReactNode } from "react";
import Providers from "./providers";



export default async function Layout({ children }: { children: ReactNode }) {
  const session = await getAuthServerSession();
  if (!session) {
    return redirect("/login");
  }
  return (
    <div className="h-screen flex">
      {/* Left Sidebar */}
      <div className="w-64 bg-teal-800 text-white p-6 flex flex-col">
        {/* Logo and Brand */}
        <div className="flex items-center gap-3 mb-8">
          <Plane size={24} className="text-teal-400" />
          <h1 className="text-2xl font-bold">Wandere.ai</h1>
        </div>

        {/* User Profile Section */}
        <div className="mb-8 p-3 bg-teal-700/50 rounded-lg">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 bg-teal-600 rounded-full flex items-center justify-center">
              <User size={20} />
            </div>
            <div>
              <h2 className="font-medium">{session.user?.name}</h2>
            </div>
          </div>
        </div>

        {/* Navigation Menu */}
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
        <button className="flex items-center gap-3 text-white/80 hover:text-white w-full p-2 rounded-lg hover:bg-teal-700 transition-colors">
          <LogOut size={20} />
          Logout
        </button>
      </div>
      <Providers>{children}</Providers>
    </div>
  );
}
