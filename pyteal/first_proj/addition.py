from pyteal import *

# define global variable to store result
result = ScratchVar()

# define function to add integers and store result in global variable
def add(a, b):
    return App.globalPut(Bytes("result"), a + b)

# define transaction conditions
txn = Gtxn[0]
condition = And(
    txn.type_enum() == TxnType.ApplicationCall,
    txn.application_id() == Int(0),
    txn.on_completion() == OnComplete.NoOp,
    Txn.application_args.length() == Int(1),
    Txn.application_args[0] == Bytes("add"),
)

# define program logic to execute the 'add' function
approval_program = If(
    condition,
    Seq(
        add(
            Btoi(Txn.application_args[1]),
            Btoi(Txn.application_args[2])
        ),
        Return(Int(1))
    ),
    Return(Int(1))
)

# CLEAR
def clear_state_program():
    return Approve()

# MAIN
if __name__ == "__main__":
    with open("addition_approval.teal", "w") as f:
        compiled = compileTeal(approval_program, mode=Mode.Application, version=5)
        f.write(compiled)

    with open("addition_clear_state.teal", "w") as f:
        compiled = compileTeal(clear_state_program(), mode=Mode.Application, version=5)
        f.write(compiled)
