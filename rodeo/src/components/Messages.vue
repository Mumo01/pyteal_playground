<template>
  <div>
    <div class="not-connected" v-if="!connected">
      <h1>Create Project</h1>
      <div >
        <p>Please connect to Algonaut to use this component.</p>
        <button @click="connect">Connect to Algonaut</button>
      </div>
    </div>

      <div class="connected" v-if="connected">
        <p>Logged in as {{account}}</p>
        <label for="receiver">Receiver:</label>
        <input type="text" id="receiver" v-model="receiverAddress">
        <label for="message">Message:</label>
        <input type="text" id="message" v-model="messageText">
        <button @click="sendMessage">Send Message</button>
        <button @click="disconnect">Disconnect From Wallet</button>
      </div>
   </div>
  </template>
  
  <script>
import { Algonaut } from '@thencc/algonautjs';

  export default {
    name: "Messages",
    components: {
    },

    data() {
      return {
        connected: false,
        account: "",
        receiverAddress: "",
        messageText: ""
      }
    },
    methods: {
     async connect() {
        // 2. create lib instance
        const algonaut = new Algonaut();

        const accounts = await algonaut.connect();
        this.account = accounts[0].address;
        this.connected = true;
      },

      async disconnect() {
        const algonaut = new Algonaut();
        await algonaut.disconnect();
        this.connected = false; 
        if (!this.connected) {
        alert('Wallet Disconnected!.');
        return;
        }

      },

    async sendMessage() {
        if (!this.connected) {
        alert('Please connect to the wallet before sending a message.');
         return;
        }

      const algonaut = new Algonaut();

     try {
    // Validate input
       if (!this.receiverAddress) {
      alert('Please enter a receiver address.');
      return;
      }

        if (!this.messageText) {
        alert('Please enter a message.');
        return;
      }

        
        // construct txn
        const txn = await algonaut.atomicSendAlgo({
        amount: 1000, // micro-algos
        to: this.receiverAddress,
        from: this.account,
        message: this.messageText, // .from needed IF algonaut isnt authenticated and doesnt have this.account populated
        });
        console.log('txn', txn, 'message', this.messageText);

        // sign + submit txn
        let txnRes = await algonaut.sendTransaction(txn);
        console.log('txnRes', txnRes);
        } catch (error) {
        console.error(error);
        alert('An error occurred while sending the message.');   
        }
    },
  }}
  </script>
  