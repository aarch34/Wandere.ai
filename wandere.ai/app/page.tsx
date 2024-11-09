import { Button } from "@/components/ui/button";
import { Map, MessageSquare, Plane, Star } from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { FeatureCard } from "./_components/feature-card";

export default async function Home() {

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="relative h-screen">
        {/* Background image */}
        <Image
          src="/img/about-img.png"
          alt="Travel background"
          fill
          className="object-cover"
          priority
        />
        {/* Overlay */}
        <div className="absolute inset-0 bg-black/50" />

        {/* Content Container */}
        <div className="relative container mx-auto px-4 h-full flex flex-col items-center justify-center">
          {/* User Session Info */}


          {/* Hero Content */}
          <div className="flex items-center justify-center min-h-[600px]">
            <div className="text-center max-w-3xl mx-auto">
            <h1 className="text-7xl font-bold text-white mb-4">
      Wandere.ai
    </h1>
    {/* Tagline */}
    <h2 className="text-3xl font-semibold text-teal-700 mb-8">
      Where AI Meets Wanderlust
    </h2>
              <p className="text-xl text-gray-100 mb-8">
                Experience travel reimagined with our intelligent companion. From hidden city gems 
                to cultural festivals, luxury resorts to local haunts - let AI craft your perfect 
                journey, your way.
              </p>
              <Button
                size="lg"
                className="bg-teal-700 hover:bg-teal-900 text-lg px-8"
                asChild
              >
                <Link href="/login">Start Exploring</Link>
              </Button>
            </div>
          </div>
        </div>
      </div>

      {/* Features Section */}
      <div className="bg-white py-24">
        <div className="container mx-auto px-4">
          <h2 className="text-3xl font-bold text-center mb-16">
            Why Choose Wandere.ai?
          </h2>
          <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
            <FeatureCard
              icon={<Plane className="w-8 h-8 text-teal-700" />}
              title="Smart Itineraries"
              description="Get personalized travel plans that match your style, budget, and dreams"
            />
            <FeatureCard
              icon={<Map className="w-8 h-8 text-teal-700" />}
              title="Local Secrets"
              description="Unlock hidden gems and authentic experiences recommended by locals"
            />
            <FeatureCard
              icon={<MessageSquare className="w-8 h-8 text-teal-700" />}
              title="24/7 Travel Companion"
              description="Your personal AI guide for instant travel advice and recommendations"
            />
            <FeatureCard
              icon={<Star className="w-8 h-8 text-teal-700" />}
              title="Customized Magic"
              description="Experience travel tailored to your unique preferences and interests"
            />
          </div>
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-teal-700 py-20">
        <div className="container mx-auto px-4 text-center">
          <h2 className="text-3xl font-bold text-white mb-6">
            Ready to Transform Your Travel Story?
          </h2>
          <p className="text-xl text-teal-50 mb-8 max-w-2xl mx-auto">
            Join thousands of travelers who've discovered the perfect blend of AI 
            intelligence and human wanderlust.
          </p>
          <Button
            variant="secondary"
            size="lg"
            className="text-teal-700 bg-white hover:bg-gray-100 text-lg px-8"
            asChild
          >
            <Link href="/login">Start Your Journey</Link>
          </Button>
        </div>
      </div>
      <footer className="bg-teal-700">
  <div className="container mx-auto px-4 py-6">
    <div className="text-center">
      <p className="text-teal-50 text-sm">
        © {new Date().getFullYear()} Wandere.ai. All rights reserved.
      </p>
    </div>
  </div>
</footer>
    </div>
  );
}