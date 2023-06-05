from pyteal import *

def approval():
    # On creation
    on_creation = Seq([
        App.globalPut(Bytes("sender"), Txn.sender()),
        Return(Int(1))
    ])
    
    handle_optin = Seq([
            Assert(Txn.application_args.length() == Int(4)),
            App.globalPut(Bytes("StartDate"), Btoi(Txn.application_args[0])),
            App.globalPut(Bytes("EndDate"), Btoi(Txn.application_args[1])),
            App.globalPut(Bytes("WorkStart"), Btoi(Txn.application_args[2])),
            App.globalPut(Bytes("WorkEnd"), Btoi(Txn.application_args[3])),
            

            Return(Int(1)),

    ])

    handle_closeout = Return(Int(0))

    handle_deleteapp = Return(Int(0))

    handle_updateapp = Return(Int(0))




    # Define the approval program
    approval_program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.on_completion() == OnComplete.UpdateApplication, handle_updateapp],
        [Txn.on_completion() == OnComplete.OptIn, handle_optin],
        [Txn.on_completion() == OnComplete.CloseOut, handle_closeout],
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_deleteapp],
    )

    return approval_program

# CLEAR
def clear_state():
    return Approve()

if __name__ == "__main__":
    with open("contract_approval.teal", "w") as f:
        compiled = compileTeal(approval(), mode=Mode.Application, version=5)
        f.write(compiled)

    with open("contract_close.teal", "w") as f:
        compiled = compileTeal(clear_state(), mode=Mode.Application, version=5)
        f.write(compiled)

    
