import prisma from "@/lib/prisma"
import { NextResponse } from "next/server"
import { GoogleGenerativeAI } from '@google/generative-ai';
import { currentUser } from "@/lib/current-user";
import { Message } from "@prisma/client";

const genAI = new GoogleGenerativeAI(process.env.GOOGLE_API_KEY!);
const model = genAI.getGenerativeModel({ model: "gemini-pro"});

const buildGoogleGenAIPrompt = (messages: Message[]) => ({
  contents: messages
    .map(message => ({
      role: message.role === 'USER' ? 'user' : 'model',
      parts: [{ text: message.content }],
    })),
});

export async function POST(req: Request){
  try {
    const user = await currentUser()
    if(!user){
      return new NextResponse('Unauthorized', {status: 401})
    }

    const {chatId, prompt} = await req.json()
    const existingChat = await prisma.chat.findUnique({
      where: {
        id: chatId,
        userId: user.id
      },
      include: {
        messages: true
      }
    })

    const messages = existingChat?.messages || []
    const processedMessages = buildGoogleGenAIPrompt(messages)

    const MODEL = model.startChat({
      history:processedMessages.contents,
      generationConfig: {
        maxOutputTokens: 100,
      },
    });
    
    const result = await MODEL.sendMessage(prompt);
    const reply = result.response.text()
    console.log('reply', reply)
    const chat = await prisma.chat.update({
      where: {
        id: chatId as string,
        userId: user.id
      },
      data: {
        messages: {
          createMany: {
            data: [
              {
                role: 'USER',
                content: prompt
              },
              {
                role: 'MODEL',
                content: reply
              }
            ]
          }
        }
      }
    })

    if(existingChat?.name === 'New Chat'){
      const NAME_MODEL = model.startChat({
        generationConfig: {
          maxOutputTokens: 5,
        },
      });

      const result = await NAME_MODEL.sendMessage('suggest name for the conversation within 3 words ' + prompt);
      const suggestedName = result.response.text()
      console.log('suggestedName', suggestedName)

      const chat = await prisma.chat.update({
        where: {
          id: chatId as string,
          userId: user.id
        },
        data: {
          name: suggestedName
        }
      })
    }

    return NextResponse.json(chat)
  } catch (error) {
    console.log(error)
    return NextResponse.json({message: 'Error chating'}, {status: 500})
  }
}