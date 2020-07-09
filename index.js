const discord = require('discord.js')
const client = new discord.Client()
const token = require('./token.js')
const { spawn } = require('child_process')
const prefix = '?'

const ask = question => {
  let stdin = Buffer.from(question).toString('base64')
  return spawn('./answer.py', [stdin])
}

const reply = ({author, content, channel}) => {
  if (content.indexOf(prefix))
    return
  
  if (author.bot) 
    return
  
  let question = content.slice(1).trim()
  let answer = ask(question)
  
  answer.stdout.on('data', data => 
    channel.send(data.toString())
  )
}

client.on('message', reply)
client.login(token)
