from pyteal import *

def approval_program():
    on_creation = Seq(
        [
            App.globalPut(Bytes("Creator"), Txn.sender()),
            Assert(Txn.application_args.length() == Int(4)),
            App.globalPut(Bytes("StartDate"), Btoi(Txn.application_args[0])),
            App.globalPut(Bytes("EndDate"), Btoi(Txn.application_args[1])),
            App.globalPut(Bytes("WorkStart"), Btoi(Txn.application_args[2])),
            App.globalPut(Bytes("WorkEnd"), Btoi(Txn.application_args[3])),
            Return(Int(1)),

        ]
    )

    handle_closeout = Return(Int(0))

    handle_deleteapp = Return(Int(0))

    is_creator = Return(Txn.sender() == App.globalGet(Bytes("Creator")))

    on_retrieve = Seq([
                App.localPut(Int(0), Bytes("AppID"), Txn.application_args[0]),
                App.localPut(Int(0), Bytes("Creator"), App.globalGet(Bytes("Creator"))),
                App.localPut(Int(0), Bytes("StartDate"), App.globalGet(Bytes("StartDate"))),
                App.localPut(Int(0), Bytes("EndDate"), App.globalGet(Bytes("EndDate"))),
                App.localPut(Int(0), Bytes("WorkStart"), App.globalGet(Bytes("WorkStart"))),
                App.localPut(Int(0), Bytes("WorkEnd"), App.globalGet(Bytes("WorkEnd"))),
                Return(Int(1))
        ]
    )

    

    program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.on_completion() == OnComplete.DeleteApplication, handle_deleteapp],
        [Txn.on_completion() == OnComplete.UpdateApplication, is_creator],
        [Txn.on_completion() == OnComplete.CloseOut, handle_closeout],
        [Txn.on_completion() == OnComplete.OptIn, on_retrieve],
    )

    return program

def clear_state_program():
    return Approve()
        
       

if __name__ == "__main__":
    with open("trial_approval.teal", "w") as f:
        compiled = compileTeal(approval_program(), mode=Mode.Application, version=5)
        f.write(compiled)

    with open("trial_clear_state.teal", "w") as f:
        compiled = compileTeal(clear_state_program(), mode=Mode.Application, version=5)
        f.write(compiled)
