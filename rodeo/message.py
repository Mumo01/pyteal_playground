from pyteal import *


def approval_program():

    # On creation of the contract
    handle_creation = Seq(
        App.globalPut(Bytes("sender"), Txn.sender()),
        Return(Int(1))
    )

    # On deletion of the contract
    on_closeout = Return(Int(1))

    # Handle message send transaction
    handle_send = Seq(
        Assert(Txn.application_args.length() == Int(1)),
        App.globalPut(Bytes("message"), Txn.application_args[0]),     # store the message in global state
        App.globalPut(Bytes("receiver"), Txn.accounts[1]),  # store the receiver account in global state
        Return(Int(1))
    )


    # Handle message read transaction
    handle_read = Seq(
        Assert(Txn.application_args.length() == Int(2)),
        Assert(Txn.accounts[1] == App.globalGet(Bytes("receiver"))),
        Return(App.globalGet(Bytes("message")))
    )

    handle_noop = Cond(
        [And(
            Global.group_size() == Int(1),
            Txn.application_args[0] == Bytes("send")
        ), handle_send],
        [And(
            Global.group_size() == Int(1),
            Txn.application_args[0] == Bytes("read")
        ), handle_read],
    )

    program = Cond(
    [Txn.application_id() == Int(0), handle_creation],
    [Txn.on_completion() == OnComplete.DeleteApplication, on_closeout],
    [Txn.on_completion() == OnComplete.NoOp, handle_noop],

    )

    return program

# CLEAR
def clear_state_program():
    return Approve()

# Compile the program
if __name__ == "__main__":
    with open("message_approval.teal", "w") as f:
        compiled = compileTeal(approval_program(), mode=Mode.Application, version=5)
        f.write(compiled)

    with open("message_clear_state.teal", "w") as f:
        compiled = compileTeal(clear_state_program(), mode=Mode.Application, version=5)
        f.write(compiled)

