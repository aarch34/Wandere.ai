"use client";
import Link from "next/link";
import { signIn } from "next-auth/react";
import {
  FaFacebookF,
  FaLinkedinIn,
  FaGoogle,
  FaRegEnvelope,
  FaUserAlt,
  FaGithub,
} from "react-icons/fa";
import { MdLockOutline } from "react-icons/md";

export default function Page() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-100 p-8">
      <div className="w-full max-w-4xl">
        <div className="bg-white rounded-2xl shadow-xl flex flex-col md:flex-row-reverse">
          {/* Left Section - Sign In Call to Action */}
          <div className="w-full md:w-2/5 bg-teal-700 text-white rounded-t-2xl md:rounded-none md:rounded-l-2xl p-8 flex flex-col justify-center items-center text-center">
            <h2 className="text-3xl font-bold">Welcome Back!</h2>
            <div className="border-2 w-16 border-white inline-block my-4"></div>
            <p className="mb-8">
              To keep connected with us please login with your personal info
            </p>
            <Link
              href="/login"
              className="border-2 border-white rounded-full px-12 py-2 hover:bg-white hover:text-teal-700 transition-colors duration-300 font-semibold"
            >
              Sign In
            </Link>
          </div>

          {/* Right Section - Sign Up Form */}
          <div className="w-full md:w-3/5 p-8">
            <div className="text-left font-bold text-black">
              <span className="text-teal-700">Wandere</span>.ai
            </div>

            <div className="mt-10">
              <h2 className="text-3xl font-bold text-teal-700">
                Create Account
              </h2>
              <div className="border-2 w-16 border-teal-700 inline-block my-4"></div>

              <div className="flex justify-center space-x-4 my-6">
                <button
                  onClick={() => signIn("facebook")}
                  className="border-2 border-gray-200 rounded-full p-3 hover:border-teal-700 transition-colors"
                >
                  <FaFacebookF className="text-sm text-gray-600" />
                </button>
                <button
                  onClick={() => signIn("linkedin")}
                  className="border-2 border-gray-200 rounded-full p-3 hover:border-teal-700 transition-colors"
                >
                  <FaLinkedinIn className="text-sm text-gray-600" />
                </button>
                <button
                  onClick={() => signIn("github")}
                  className="border-2 border-gray-200 rounded-full p-3 hover:border-teal-700 transition-colors"
                >
                  <FaGithub className="text-sm text-gray-600" />
                </button>
                <button
                  onClick={() => signIn("google")}
                  className="border-2 border-gray-200 rounded-full p-3 hover:border-teal-700 transition-colors"
                >
                  <FaGoogle className="text-sm text-gray-600" />
                </button>
              </div>

              <p className="text-gray-600 text-center my-4">
                or use your email for registration
              </p>

              <form className="flex flex-col items-center space-y-4">
                <div className="bg-gray-100 w-full max-w-sm p-2 flex items-center rounded">
                  <FaUserAlt className="text-gray-400 mx-2" />
                  <input
                    type="text"
                    name="name"
                    placeholder="Name"
                    className="bg-gray-100 outline-none text-sm flex-1 text-black placeholder-gray-400"
                  />
                </div>

                <div className="bg-gray-100 w-full max-w-sm p-2 flex items-center rounded">
                  <FaRegEnvelope className="text-gray-400 mx-2" />
                  <input
                    type="email"
                    name="email"
                    placeholder="Email"
                    className="bg-gray-100 outline-none text-sm flex-1 text-black placeholder-gray-400"
                  />
                </div>

                <div className="bg-gray-100 w-full max-w-sm p-2 flex items-center rounded">
                  <MdLockOutline className="text-gray-400 mx-2" />
                  <input
                    type="password"
                    name="password"
                    placeholder="Password"
                    className="bg-gray-100 outline-none text-sm flex-1 text-black placeholder-gray-400"
                  />
                </div>

                <div className="bg-gray-100 w-full max-w-sm p-2 flex items-center rounded">
                  <MdLockOutline className="text-gray-400 mx-2" />
                  <input
                    type="password"
                    name="confirmPassword"
                    placeholder="Confirm Password"
                    className="bg-gray-100 outline-none text-sm flex-1 text-black placeholder-gray-400"
                  />
                </div>

                <button
                  type="submit"
                  className="border-2 border-teal-700 text-teal-700 rounded-full px-12 py-2 hover:bg-teal-700 hover:text-white transition-colors duration-300 font-semibold mt-4"
                >
                  Sign Up
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
