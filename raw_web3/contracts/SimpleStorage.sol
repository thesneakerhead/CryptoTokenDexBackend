// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.8.0;

contract SimpleStorage{
     struct People{
        uint256 favouriteNumber;
        string name;
    }

    uint256 favouriteNumber;
    People [] public people;
    mapping(string=>uint256) public nameToFavouriteNumber;
   

    People public person = People({favouriteNumber:2,name:"Patrick"});

    function store(uint256 _favouriteNumber) external{
        favouriteNumber = _favouriteNumber;
        
    }

    function retrieve() public view returns(uint256){
        return favouriteNumber;
    }   
    
    function addPerson(string memory _name, uint256 _favouriteNumber) public {
        people.push(People({favouriteNumber:_favouriteNumber,name:_name}));
        nameToFavouriteNumber[_name]=_favouriteNumber;
    }
}