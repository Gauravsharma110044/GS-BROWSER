"use client"
import GithubLoginButton from '@/components/auth/GithubLoginButton';
import GoogleLoginButton from '@/components/auth/GoogleLoginButton';
import { Button, buttonVariants } from '@/components/ui/button';
import { Form, FormControl, FormField, FormItem, FormLabel, FormMessage } from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Separator } from '@/components/ui/separator';
import { toast } from '@/components/ui/use-toast';
import { cn } from '@/lib/utils';
import { zodResolver } from '@hookform/resolvers/zod';
import { useRouter } from 'next/navigation';
import React from 'react'
import { useForm } from 'react-hook-form';
import * as z from 'zod'

const FormSchema = z
  .object({
    name: z.string().min(1, "Name is required!"),
    email: z.string().min(1, "Email is required!").email("Invalid email!"),
    password: z
      .string()
      .min(1, "Password is required!")
      .min(8, "Password must have than 8 characters!"),
    confirmPassword: z.string().min(1, "Password confirmation is required!"),
  })
  .refine((data) => data.password === data.confirmPassword, {
    path: ["confirmPassword"],
    message: "Password do not match!",
});


const page = () => {
  const router = useRouter()
  const form = useForm<z.infer<typeof FormSchema>>({
    resolver: zodResolver(FormSchema),
    defaultValues: {
      name: "",
      email: "",
      password: "",
      confirmPassword: "",
    },
  });
  const isLoading = form.formState.isSubmitting
  const onSubmit = async (values: z.infer<typeof FormSchema>) => {
    const response = await fetch("/api/auth/register", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email: values.email,
        password: values.password,
        name: values.name
      }),
    });

    if (response.ok) {
      router.push("/login");
      router.refresh()
    } else {
      toast({
        title: "Error",
        description: "Oops! Something went wrong!",
      });
    }
  };

  return (
    <div className='space-y-4'>
      <h3 className='font-bold text-3xl text-center'>Create An Account</h3>
      <Form {...form}>
        <form className='space-y-4' onSubmit={form.handleSubmit(onSubmit)}>
          <FormField 
            control={form.control}
            name='name'
            render={(({field}) => (
              <FormItem>
                <FormControl>
                  <Input className='focus-visible:ring-0 focus-visible:ring-offset-0 focus:border-emerald-400' placeholder='Your Name' {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            ))}
          />
          <FormField 
            control={form.control}
            name='email'
            render={(({field}) => (
              <FormItem>
                <FormControl>
                  <Input className='focus-visible:ring-0 focus-visible:ring-offset-0 focus:border-emerald-400' placeholder='Email Address' {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            ))}
          />
          <FormField 
            control={form.control}
            name='password'
            render={(({field}) => (
              <FormItem>
                <FormControl>
                  <Input disabled={isLoading} className='focus-visible:ring-0 focus-visible:ring-offset-0 focus:border-emerald-400' placeholder='Enter Password' type='password' {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            ))}
          />
          <FormField 
            control={form.control}
            name='confirmPassword'
            render={(({field}) => (
              <FormItem>
                <FormControl>
                  <Input disabled={isLoading} className='focus-visible:ring-0 focus-visible:ring-offset-0 focus:border-emerald-400' placeholder='Re-enter Password' type='password' {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            ))}
          />
          <Button variant='green' type='submit' disabled={isLoading} className='w-full'>Sign Up</Button>
        </form>
      </Form>
      <div className='text-center'>
        Already have an account? <span onClick={() => router.push('/login')} className={cn(buttonVariants({variant: 'link'}), 'text-emerald-500 cursor-pointer')}>Sign In</span>
      </div>
      <Separator className='h-[2px]' />
      <div className='space-y-2'>
        <GoogleLoginButton />
        <GithubLoginButton />
      </div>
    </div>
  )
}

export default page
