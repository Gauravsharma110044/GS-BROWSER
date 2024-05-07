"use client"
import React from 'react'
import { Input } from '../ui/input'
import { useForm } from 'react-hook-form'
import * as z from 'zod'
import { zodResolver } from '@hookform/resolvers/zod'
import { Form, FormControl, FormField, FormItem } from '../ui/form'
import { ArrowUp } from 'lucide-react'
import { Chat, Message } from '@prisma/client'
import axios from 'axios'
import { useRouter } from 'next/navigation'
const FormSchema = z.object({
  prompt: z.string().min(1)
})

interface ChatInputProps {
  chat: Chat & {
    messages: Message[]
  }
}

const ChatInput = ({chat}: ChatInputProps) => {
  const router = useRouter()
  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      prompt: ""
    }
  })
  const isLoading = form.formState.isSubmitting
  const onSubmit = async (values: z.infer<typeof FormSchema>) => {
    try {
      const response = await axios.post('/api/chat', {chatId: chat.id, prompt: values.prompt})
      console.log(response)  
      router.refresh()
      form.reset()
    } catch (error) {
      console.log(error)
    }
  }
  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)}>
        <FormField
          control={form.control}
          name='prompt'
          disabled={isLoading}
          render={(({field}) => (
            <FormItem>
              <FormControl>
                <div className='relative p-4 px-6'>
                  <Input placeholder="Message ChatGPT" {...field} disabled={isLoading} className='px-6 py-7 bg-zinc-200/90 dark:bg-[#212121] border border-zinc-600 focus-visible:ring-0 focus-visible:ring-offset-0 text-zinc-600 dark:text-gray-300 rounded-xl' autoFocus />
                  <button disabled={form.getValues('prompt') === ''} type='submit' className='cursor-pointer bg-white rounded-xl text-black p-2 absolute top-7 right-8'>
                    <ArrowUp className='w-5 h-5' />
                  </button>
                </div>
              </FormControl>
            </FormItem>
          ))}
        />
      </form>
    </Form>
  )
}

export default ChatInput
