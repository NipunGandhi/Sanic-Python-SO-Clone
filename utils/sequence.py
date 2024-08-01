from db import Sequence


async def get_next_sequence_value(sequence_name: str) -> str:
    sequence = await Sequence.find_one(Sequence.name == sequence_name)

    if not sequence:
        sequence = Sequence(name=sequence_name, sequence_value=0)
        await sequence.insert()

    sequence.sequence_value += 1
    await sequence.save()

    user_id = f"MG{sequence.sequence_value:05d}"
    return user_id
