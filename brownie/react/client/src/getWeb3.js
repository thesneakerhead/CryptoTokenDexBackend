import Web3 from "web3";
import {getEthereum} from "./getEthereum";

export const getWeb3 = async () => {

    const ethereum = await getEthereum()
    let web3
    // if detect metamask chain provider
    if (ethereum) {
        web3 = new Web3(ethereum)
    } else if (window.web3) {
        web3 = window.web3
    }
    // else use localhost 
    else {
        const provider = new Web3.providers.HttpProvider(
            "http://127.0.0.1:8545"
        );
        web3 = new Web3(provider)
    }

    return web3
}