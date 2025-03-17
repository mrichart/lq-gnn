import ignnition


def main():
    model = ignnition.create_model(model_dir='./')
    #model.computational_graph()
    #model.train_and_validate()
    model.evaluate()
    # model.predict()


if __name__ == "__main__":
    main()
