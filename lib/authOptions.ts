import { NextAuthOptions } from 'next-auth'
import GoogleProvider from 'next-auth/providers/google'
import GithubProvider from 'next-auth/providers/github'
import { PrismaAdapter } from '@auth/prisma-adapter'
import prisma from './prisma'

// Debug environment variables
console.log('Auth Configuration Debug:');
console.log('GITHUB_ID:', process.env.GITHUB_ID ? 'Set' : 'Not Set');
console.log('GITHUB_SECRET:', process.env.GITHUB_SECRET ? 'Set' : 'Not Set');
console.log('NEXTAUTH_URL:', process.env.NEXTAUTH_URL);
console.log('NEXTAUTH_SECRET:', process.env.NEXTAUTH_SECRET ? 'Set' : 'Not Set');

export const authOptions: NextAuthOptions = {
  debug: true, // Enable debug mode
  adapter: PrismaAdapter(prisma),
  providers: [
    GoogleProvider({
      clientId: process.env.GOOGLE_CLIENT_ID || '',
      clientSecret: process.env.GOOGLE_CLIENT_SECRET || '',
    }),
    GithubProvider({
      clientId: process.env.GITHUB_ID || '',
      clientSecret: process.env.GITHUB_SECRET || '',
    }),
  ],
  session: {
    strategy: 'jwt',
  },
  pages: {
    signIn: '/login',
  },
  callbacks: {
    async session({ session, token }) {
      if (session.user) {
        session.user.id = token.sub as string;
      }
      return session;
    },
    async signIn({ user, account, profile }) {
      console.log('Sign In Debug:', { user, account, profile });
      return true;
    },
  },
}