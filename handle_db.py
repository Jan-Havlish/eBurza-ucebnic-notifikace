def get_docs(db, col_name):
    col_ref = db.collection(col_name)
    docs = col_ref.stream()

    docs_dict = {}
    for doc in docs:
        print(f"{doc.id} => {doc.to_dict()}")
        docs_dict[doc.id] = doc.to_dict()
    return docs_dict

def del_doc(db, col_name, key):
    col_ref = db.collection(col_name)
    doc_ref = col_ref.document(key)

    try:
        doc_ref.delete()
        print(f"Document with key {key} successfully deleted.")
        return True
    except Exception as e:
        print(f"An error occurred while deleting the document: {e}")
        return False
