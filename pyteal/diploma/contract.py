from pyteal import *
from pyteal.ast.bytes import Bytes

# Declare application GLOBAL state storage (immutable)
global_registrar = Bytes("registrar")
local_diploma = Bytes("diploma")

def approval():
  # Code block invoked during contract initialization. Sets the
  # registrar to be the sender (creator) of this smart contract
  init_contract = Seq([
    App.globalPut(global_registrar, Txn.sender()),
    Return(Int(1))
  ])

  # Checks if the sender of the current transaction invoking this
  # smart contract is the current registrar
  is_registrar = Txn.sender() == App.globalGet(global_registrar)

  # Code block invoked during diploma issuance. Only the registrar
  # may invoke this block with two arguments and one account supplied.
  # The first argument was "register_diploma" used by the control flow 
  # below. The second argument is the diploma metadata which is
  # set to the local storage of the supplied account
  diploma_metadata = Txn.application_args[1]
  diploma_receiver = Txn.accounts[1]

  register_diploma = Seq([
      Assert(is_registrar),
      App.localPut(diploma_receiver, local_diploma, diploma_metadata),
      Return(Int(1))
  ])


  program = Cond(
    # Control flow logic of the smart contract
    [Txn.application_id() == Int(0), init_contract],
    [Txn.on_completion() == OnComplete.OptIn, Return(Int(1))],
    [Txn.on_completion() == OnComplete.CloseOut, Return(Int(1))],
    [Txn.application_args[0] == Bytes("register_diploma"), register_diploma]
  )

  return program


def clear():
  return Return(
    Int(1)
  )
  
if __name__ == '__main__':
  import os

  path = os.path.dirname(os.path.abspath(__file__))

  with open(os.path.join(path, "approval.teal"), "w") as f:
    f.write(compileTeal(approval(), mode=Mode.Application, version=6))
    
  with open(os.path.join(path, "clear.teal"), "w") as f:
    f.write(compileTeal(clear(), mode=Mode.Application, version=6))