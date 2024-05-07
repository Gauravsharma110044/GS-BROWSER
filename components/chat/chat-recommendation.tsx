"use client"
import React from 'react'
import BotAvatar from '../bot-avatar'
import { Chat, Message } from '@prisma/client'
import axios from 'axios'
import { useRouter } from 'next/navigation'

interface ChatRecommendationProps {
  chat: Chat & {
    messages: Message[]
  }
}

type Recommendation = {
  title: string;
  sub: string;
}

const recommendations: Recommendation[] = [
  {
    title: "Make me a personal webpage",
    sub: "after asking me three questions"
  },
  {
    title: "Suggest fun activities",
    sub: "to help me make friends in a new city"
  },
  {
    title: "Write an email",
    sub: "to request a quote from local plumbers"
  },
  {
    title: "Create a morning routine",
    sub: "to boost my productivity"
  }
];

const ChatRecommendation = ({chat}: ChatRecommendationProps) => {
  const router = useRouter()
  const start = async (recommendation: Recommendation) => {
    try {
      const response = await axios.post('/api/chat', {chatId: chat.id, prompt: recommendation.title + ' ' + recommendation.sub})
      router.refresh()
    } catch (error) {
      console.log(error)
    }
  }
  return (
    <div className='flex flex-col flex-1 justify-center items-center'>
      <div className='flex flex-col items-center space-y-5 fixed'>
        <BotAvatar className='w-10 h-10' />
        <h2 className='text-2xl font-semibold'>How can I help you today?</h2>
      </div>

      <div className='grid grid-cols-2 gap-2 w-full mt-auto'>
        {recommendations.map((recommendation) => {
          return (
            <button onClick={() => start(recommendation)} className='text-left pl-4 px-2 py-4 border-zinc-600 border rounded-xl hover:bg-zinc-700/30 transition'>
              <p className='font-bold'>{recommendation.title}</p>
              <span className='text-sm text-gray-300'>{recommendation.sub}</span>
            </button>
          )
        })}
      </div>
    </div>
  )
}

export default ChatRecommendation
