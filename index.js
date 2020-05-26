const discord = require('discord.js')
const client = new discord.Client()
const token = require('./token.js')
const { spawn } = require('child_process')
const prefix = '?'


client.on('ready', () => {
    console.log(`info: connected as ${client.user.tag}`)
})



client.on('message', message => {
    if (message.author.bot) {
      return
    }
    
    if (message.content.indexOf(prefix) !== 0) {
      return
    }

    let question = message.content.slice(1).trim()
    console.log(`info: someone asked a question - ${question}`)

    let input = Buffer.from(question).toString('base64')
    let answer = spawn('./ask.py', [input])
    
    answer.stdout.on('data', data => {
      message.channel.send(data.toString())
    })
    
    console.log(`info: answer was sent back`)
})



client.login(token)
