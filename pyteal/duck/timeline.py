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

    is_creator = Txn.sender() == App.globalGet(Bytes("Creator"))

    get_sender_acceptance = App.localGetEx(Int(0), App.id(), Bytes("accepted"))
    
    on_closeout = Seq(
        [
            get_sender_acceptance,
            If(
                And(
                    Global.round() <= App.globalGet(Bytes("WorkEnd")),
                    get_sender_acceptance.hasValue(),
                ),
                App.globalPut(
                    get_sender_acceptance.value(),
                    App.globalGet(get_sender_acceptance.value()) + Int(1),
                ),
            ),
            Return(Int(1)),
        ]
    )

    on_work_submission = Return(
        And(
            Global.round() >= App.globalGet(Bytes("StartDate")),
            Global.round() <= App.globalGet(Bytes("EndDate")),
        )
    )

    choice = Txn.application_args[1]
    choice_tally = App.globalGet(choice)
    on_choosing = Seq(
        [
            Assert(
                And(
                    Global.round() >= App.globalGet(Bytes("WorkStart")),
                    Global.round() <= App.globalGet(Bytes("WorkEnd")),
                )
            ),
            get_sender_acceptance,
            If(get_sender_acceptance.hasValue(), Return(Int(1))),
            App.globalPut(choice, choice_tally + Int(1)),
            App.localPut(Int(0), Bytes("accepted"), choice),
            Return(Int(1)),
        ]
    )

    program = Cond(
        [Txn.application_id() == Int(0), on_creation],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(is_creator)],
        [Txn.on_completion() == OnComplete.UpdateApplication, is_creator],
        [Txn.on_completion() == OnComplete.OptIn, on_work_submission],
        [Txn.application_args[0] == Bytes("accepted"), on_choosing],
    )

    return program

def clear_state_program():
    get_sender_acceptance = App.localGetEx(Int(0), App.id(), Bytes("accepted"))
    program = Seq(
        [
            get_sender_acceptance,
            If(
                And(
                    Global.round() <= App.globalGet(Bytes("WorkEnd")),
                    get_sender_acceptance.hasValue(),
                ),
                App.globalPut(
                    get_sender_acceptance.value(),
                    App.globalGet(get_sender_acceptance.value()) - Int(1),
                ),
            ),
            Return(Int(1)),
        ]
    )

    return program


if __name__ == "__main__":
    with open("time_approval.teal", "w") as f:
        compiled = compileTeal(approval_program(), mode=Mode.Application, version=5)
        f.write(compiled)

    with open("time_clear_state.teal", "w") as f:
        compiled = compileTeal(clear_state_program(), mode=Mode.Application, version=5)
        f.write(compiled)

