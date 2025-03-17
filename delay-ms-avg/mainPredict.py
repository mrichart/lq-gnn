import ignnition


def main():
    model = ignnition.create_model(model_dir='./')
    #model.computational_graph()
    #model.train_and_validate()
    #model.evaluate()
    predictions = model.predict(num_predictions=1)
    print(predictions)


if __name__ == "__main__":
    main()
