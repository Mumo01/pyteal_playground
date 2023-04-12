from pyteal import *


# Define the stateful smart contract
def stateful_contract():

    # Define the project struct
    project_struct = Tuple([
        Bytes('project_name'),
        Bytes('project_description'),
        Bytes('start_date'),
        Bytes('end_date'),
        Int('reward')
    ])

    # Define the global state for the project
    global_state = App.globalPut(
        Bytes('project_count'), Int(0)
    )

# Define the create_project transaction
    create_project = And(
    # Check if the create_project transaction is called in a handle_noop condition
    Global.group_size() == Int(1),
    Txn.application_args.length() == Int(6),
    Txn.application_args[0] == Bytes('create'),

    # Retrieve the project details from the transaction arguments
    project_name = Txn.application_args[1],
    project_description = Txn.application_args[2],
    start_date = Txn.application_args[3],
    end_date = Txn.application_args[4],
    reward = Btoi(Txn.application_args[5])
)

    project_id = App.globalGet(Bytes('project_count'))

    create_project = And(
    create_project,
    # Generate a new project ID
    App.globalPut(Bytes('project_count'), project_id + Int(1)),
    # Store the project details in the application local state
    App.localPut(Int(project_id), project_struct.pack(
        project_name,
        project_description,
        start_date,
        end_date,
        reward
    )),
    Return(Int(1))
)

    # Define the application logic
    program = Cond(
        [Txn.application_id() == Int(0), global_state],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop],
        [Txn.type_enum() == TxnType.DeleteApplication, Return(global_state)],
        [Txn.type_enum() == TxnType.ApplicationCall, Return(Int(0))]
    )

    return program


# Define the handle_noop function
def handle_noop():

    # Check if the first argument is the string 'create'
    create = And(
        Txn.application_args[0] == Bytes("create"),
        create_project
    )

    return create


# Create the stateful smart contract
if __name__ == "__main__":
    with open('stateful.teal', 'w') as f:
        compiled = compileTeal(stateful_contract(), mode=Mode.Application, version=4)
        f.write(compiled)
